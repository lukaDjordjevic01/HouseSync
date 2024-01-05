import {Box, Button, useTheme} from "@mui/material";
import {useState} from "react";
import axios from "axios";
import {Device} from "../model.ts";

export default function Scenarios (){
  
    const theme = useTheme();
    
    const [ds1Locked, setDs1Locked] = useState<boolean>(true);
    const [ds2Locked, setDs2Locked] = useState<boolean>(true);
    
    const handleDs1Click = () => {
        setDs1Locked(prevState => !prevState);
        axios.post<any>("http://localhost:5000/ds", {device_id: "DS1"})
            .then(res => {
                if (res.status === 200) {
                    console.log(res);
                }
            })
            .catch(err => {
                console.log(err);
            });
    }
    const handleDs2Click = () => {
        setDs2Locked(prevState => !prevState);
        axios.post<any>("http://localhost:5000/ds", {device_id: "DS2"})
            .then(res => {
                if (res.status === 200) {
                    console.log(res);
                }
            })
            .catch(err => {
                console.log(err);
            });
    }
    
    const handleDmsClick = (scenario: string) => {
        axios.post<any>("http://localhost:5000/dms-pin", {scenario: scenario})
            .then(res => {
                if (res.status === 200) {
                    console.log(res);
                }
            })
            .catch(err => {
                console.log(err);
            });
    }
    
    return(
      <Box sx={{
          display: "flex",
          flexDirection: "column",
          gap: "20px",
          alignItems: "center",
          width: "100%"
      }}>
          <h1>Simulation scenarios</h1>
          <Box sx={{
              display: "flex",
              flexDirection: "column",
              width: "100%",
              alignItems: "center"
          }}>
              <h2>Door sensors</h2>
              <Box sx={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  width: "100%",
                  gap: "20px"
              }}>
                  <Box sx={{
                      width: "40%"
                  }}>
                      <h3>DS1</h3>
                      <Button variant="contained" sx={{
                          textTransform: "capitalize",
                          width: "100%"
                      }}
                              onClick={handleDs1Click}
                      >{ds1Locked ? "Unlock" : "Lock"}</Button>
                  </Box>
                  <Box sx={{
                      width: "40%"
                  }}>
                      <h3>DS2</h3>
                      <Button variant="contained" sx={{
                          textTransform: "capitalize",
                          width: "100%"
                      }}
                              onClick={handleDs2Click}
                      >{ds2Locked ? "Unlock" : "Lock"}</Button>
                  </Box>
              </Box>
          </Box>
          <Box sx={{
              display: "flex",
              flexDirection: "column",
              width: "100%",
              alignItems: "center"
          }}>
              <h2>Door membrane switch</h2>
              <Box sx={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  width: "100%",
                  gap: "20px"
              }}>
                  <Button variant="contained" sx={{
                      textTransform: "capitalize",
                      width: "40%"
                  }}
                          onClick={() => handleDmsClick("correct")}
                  >Correct</Button>
                  <Button variant="contained" sx={{
                      textTransform: "capitalize",
                      width: "40%"
                  }}
                          onClick={() => handleDmsClick("incorrect")}
                  >Incorrect</Button>
              </Box>
          </Box>
      </Box>
  )
}