import express from 'express';
import router from './routes/queryRouter.js';
const app = express();
const PORT = 3000;

app.use(express.json())
app.use(express.urlencoded({extended: true}));
app.use("/repos", router);

app.listen(PORT, ()=> {
    console.log("Starting server...");
})
