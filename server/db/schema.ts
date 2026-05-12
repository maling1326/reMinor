import { int, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const FruitsTable = sqliteTable("Fruits", {
  id: int().primaryKey({ autoIncrement: true }),
  name: text().notNull(),
});
