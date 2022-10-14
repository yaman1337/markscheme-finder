import fetch from "node-fetch";
import express from "express";
import cors from "cors";

const app = express();
app.use(cors({origin: ["*"]}));
app.use(express.static("public"));

app.get("/", (req, res) => {
  res.sendFile("/index.html");
});

app.get("/api", async (req, res) => {
  try {
    let { season, year, variant } = req.query;
    season = season.toLowerCase();
    year = parseInt(year);
    let url = `https://dynamicpapers.com/wp-content/uploads/2015/09/9702_${season}${
      year < 10 ? 0 : ""
    }${year}_ms_${variant}.pdf`;
    
    let paper = parseInt(variant.split("")[0]);

    if (year === 4 && season === "s") {
      url = `https://dynamicpapers.com/wp-content/uploads/2015/09/9702_${season}0${year}_ms.pdf`;
    } else if (year === 2 || (year <= 9 && year >= 4)) {
      url = `https://dynamicpapers.com/wp-content/uploads/2015/09/9702_${season}0${year}_ms_${paper}.pdf`;
    } else if (year === 4 && season === "s") {
      url = `https://dynamicpapers.com/wp-content/uploads/2015/09/9702_${season}0${year}_ms.pdf`;
    } else if (year < 4) {
      url = `https://dynamicpapers.com/wp-content/uploads/2015/09/9702_${season}0${year}_ms_1-2-3-4-5-6.pdf`;
    }

    const resp = await fetch(url);

    if (resp.status > 300) {
      return res.status(404).json({ error: "Marks scheme not found" });
    }

    const data = await resp.arrayBuffer();
    const final =
      "data:application/pdf;base64, " + Buffer.from(data).toString("base64");
    res.statusCode = 200
    res.send(final);
  } catch (error) {
    console.log(error);
    res.send(error);
  }
});

app.listen(process.env.PORT || 9000, () => {
  console.log("Listening on port 9000");
});
