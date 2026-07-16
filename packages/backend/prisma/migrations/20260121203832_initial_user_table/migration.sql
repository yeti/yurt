-- CreateExtension
CREATE EXTENSION IF NOT EXISTS citext;

-- CreateTable
CREATE TABLE "user" (
    "id" SERIAL NOT NULL,
    "email" CITEXT NOT NULL,
    "first_name" TEXT,

    CONSTRAINT "user_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "user_email_key" ON "user"("email");
