-- CreateTable
CREATE TABLE "requests_details" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "url" TEXT NOT NULL,
    "type" TEXT NOT NULL,
    "size" REAL NOT NULL,
    "ecoindex_id" TEXT,
    CONSTRAINT "requests_details_ecoindex_id_fkey" FOREIGN KEY ("ecoindex_id") REFERENCES "api_ecoindex" ("id") ON DELETE SET NULL ON UPDATE CASCADE
);
