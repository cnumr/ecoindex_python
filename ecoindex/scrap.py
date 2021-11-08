from datetime import datetime
from json import loads
from sys import getsizeof
from typing import Optional, Tuple
from warnings import filterwarnings

import undetected_chromedriver.v2 as uc
from pydantic.networks import HttpUrl
from selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium.webdriver import Chrome, DesiredCapabilities

from ecoindex.ecoindex import get_ecoindex
from ecoindex.models import Page, PageMetrics, PageType, Result, WindowSize


async def get_page_analysis(
    url: HttpUrl,
    window_size: Optional[WindowSize] = WindowSize(width=1920, height=1080),
    wait_before_scroll: Optional[int] = 1,
    wait_after_scroll: Optional[int] = 1,
) -> Result:
    filterwarnings(action="ignore")
    page_metrics, page_type = await scrap_page(
        url=url,
        window_size=window_size,
        wait_before_scroll=wait_before_scroll,
        wait_after_scroll=wait_after_scroll,
    )
    ecoindex = await get_ecoindex(
        dom=page_metrics.nodes, size=page_metrics.size, requests=page_metrics.requests
    )
    return Result(
        score=ecoindex.score,
        ges=ecoindex.ges,
        water=ecoindex.water,
        grade=ecoindex.grade,
        url=url,
        date=datetime.now(),
        width=window_size.width,
        height=window_size.height,
        nodes=page_metrics.nodes,
        size=page_metrics.size,
        requests=page_metrics.requests,
        page_type=page_type,
    )


async def scrap_page(
    url: HttpUrl,
    window_size: WindowSize,
    wait_before_scroll: int,
    wait_after_scroll: int,
) -> Tuple[PageMetrics, PageType]:
    chrome_options = uc.ChromeOptions()
    chrome_options.headless = True
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"--window-size={window_size}")

    capbs = DesiredCapabilities.CHROME.copy()
    capbs["goog:loggingPrefs"] = {"performance": "ALL"}

    driver = uc.Chrome(options=chrome_options, desired_capabilities=capbs)

    driver.set_script_timeout(10)
    driver.get(url)
    driver.implicitly_wait(wait_before_scroll)
    try:
        driver.execute_script(
            "window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })"
        )
    except JavascriptException:
        pass

    driver.implicitly_wait(wait_after_scroll)

    page_type = await get_page_type(driver)
    page_metrics = await get_page_metrics(driver)

    driver.quit()

    return page_metrics, page_type


async def get_page_metrics(driver: Chrome) -> PageMetrics:
    page = Page(
        logs=driver.get_log("performance"),
        outer_html=driver.execute_script("return document.documentElement.outerHTML"),
        nodes=driver.find_elements_by_xpath("//*"),
    )
    downloaded_data = [
        loads(log["message"])["message"]["params"]["encodedDataLength"]
        for log in page.logs
        if "INFO" == log["level"] and "Network.loadingFinished" in log["message"]
    ]

    return PageMetrics(
        size=(sum(downloaded_data) + getsizeof(page.outer_html)) / (10 ** 3),
        nodes=len(page.nodes),
        requests=len(downloaded_data),
    )


async def get_page_type(driver: Chrome) -> Optional[PageType]:
    try:
        page_type = driver.find_element_by_xpath(
            "//meta[@property='og:type']"
        ).get_attribute("content")
    except (NoSuchElementException):
        page_type = None

    return page_type
