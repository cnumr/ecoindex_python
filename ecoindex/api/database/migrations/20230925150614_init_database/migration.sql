-- CreateTable
CREATE TABLE "api_ecoindex" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "date" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "url" TEXT NOT NULL,
    "host" TEXT NOT NULL,
    "width" INTEGER NOT NULL,
    "height" INTEGER NOT NULL,
    "size" REAL NOT NULL,
    "nodes" INTEGER NOT NULL,
    "requests" INTEGER NOT NULL,
    "grade" TEXT NOT NULL,
    "score" REAL NOT NULL,
    "ges" REAL NOT NULL,
    "water" REAL NOT NULL,
    "page_type" TEXT NOT NULL,
    "initial_ranking" INTEGER NOT NULL,
    "initial_total_results" INTEGER NOT NULL,
    "version" INTEGER NOT NULL,
    "ecoindex_version" TEXT NOT NULL
);

-- CreateIndex
CREATE INDEX "api_ecoindex_url_host_date_idx" ON "api_ecoindex"("url", "host", "date" DESC);
