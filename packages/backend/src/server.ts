import app from "./app.js";

app.listen(process.env.PORT || "8080", () => {
  console.log("Server started");
});
