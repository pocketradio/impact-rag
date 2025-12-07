import { Router } from "express";
const router = Router();

router.post("/index",(req,res,next)=>{
    console.log('here.');
    fetch('http://localhost:8000/ingest')
    .then((response)=> console.log(response.json));                                                                                     
})

router.post("/query",(req,res,next)=>{
    
})

export default router;