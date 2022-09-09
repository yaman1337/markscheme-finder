import fetch from "node-fetch";
import express from "express";
import cors from "cors"

const app = express();
app.use(cors())
app.use(express.static("public"))

app.get("/", (req, res) => {
    res.sendFile("/index.html")
})

app.get("/api", async (req, res) => {
    try {

        let {season, year, variant} = req.query;
        season = season.toLowerCase()

        const resp = await fetch(
            `https://dynamicpapers.com/wp-content/uploads/2015/09/9702_${season}${year}_ms_${variant}.pdf`
          );
          
          if(resp.status > 300) {
           return res.status(404).json({error: "Pastpaper not found"})
          }

          const data = await resp.arrayBuffer()
          const final = "data:application/pdf;base64, "+Buffer.from(data).toString('base64');
          res.send(final)
    } catch (error) {
        console.log(error);
        res.send(error)
    }
})

app.listen(9000, () => {
    console.log("Listening on port 9000")
})