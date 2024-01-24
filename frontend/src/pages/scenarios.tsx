import {Box, Button, FormControl, InputLabel, MenuItem, Select, SelectChangeEvent, useTheme} from "@mui/material";
import {useState} from "react";
import axios from "axios";
import {Device} from "../model.ts";

export default function Scenarios (){
  
    const theme = useTheme();
    
    const [ds1Locked, setDs1Locked] = useState<boolean>(true);
    const [ds2Locked, setDs2Locked] = useState<boolean>(true);
    
    const [dusId, setDusId] = useState<string>("DUS1");
    const [rpirId, setRpirId] = useState<string>("RPIR1");
    
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
    
    const handleDusClick = (scenario: string) => {
        axios.post<any>("http://localhost:5000/dus", {device_id: dusId, scenario: scenario})
            .then(res => {
                if (res.status === 200) {
                    console.log(res);
                }
            })
            .catch(err => {
                console.log(err);
            });
    }
    
    const handleDusIdChange = (event: SelectChangeEvent) => {
        setDusId(event.target.value);
    }
    
    const handleRpirIdChange = (event: SelectChangeEvent) => {
        setRpirId(event.target.value);
    }

    const handleGsgClick = () => {
        axios.post<any>("http://localhost:5000/acceleration")
            .then(res => {
                if (res.status === 200) {
                    console.log(res);
                }
            })
            .catch(err => {
                console.log(err);
            });
    }
    
    const handleRpirClick = () => {
        axios.post<any>("http://localhost:5000/rpir", {device_id: rpirId})
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
          
          <Box sx={{
              display: "flex",
              flexDirection: "column",
              width: "100%",
              alignItems: "center",
              gap: "10px"
          }}>
              <h2>People entering/exiting</h2>
              <Select
                  labelId="demo-simple-select-label"
                  id="demo-simple-select"
                  value={dusId}
                  onChange={handleDusIdChange}
                  label="Devices"
                  sx={{
                      backgroundColor: theme.palette.primary.main,
                      color: theme.palette.primary.contrastText
                  }}
                  MenuProps={{
                      PaperProps: {
                          sx: {
                              backgroundColor: theme.palette.primary.main,
                              '& .MuiMenuItem-root': {
                                  backgroundColor: theme.palette.primary.main,
                              },
                          },
                      },
                  }}
              >
                  <MenuItem
                      value="DUS1"
                  >
                      DUS1 and DPIR1
                  </MenuItem>
                  <MenuItem
                      value="DUS2"
                  >
                      DUS2 and DPIR2
                  </MenuItem>
              </Select>
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
                          onClick={() => handleDusClick("in")}
                  >Person entering</Button>
                  <Button variant="contained" sx={{
                      textTransform: "capitalize",
                      width: "40%"
                  }}
                          onClick={() => handleDusClick("out")}
                  >Person exiting</Button>
              </Box>
          </Box>
          
          <Box sx={{
              display: "flex",
              flexDirection: "column",
              width: "100%",
              alignItems: "center",
              gap: "10px"
          }}>
              <h2>RPIR triggers</h2>
              <Box sx={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  width: "100%",
                  gap: "20px"
              }}>
                  <Select
                      labelId="demo-simple-select-label"
                      id="demo-simple-select"
                      value={rpirId}
                      onChange={handleRpirIdChange}
                      label="Devices"
                      sx={{
                          backgroundColor: theme.palette.primary.main,
                          color: theme.palette.primary.contrastText
                      }}
                      MenuProps={{
                          PaperProps: {
                              sx: {
                                  backgroundColor: theme.palette.primary.main,
                                  '& .MuiMenuItem-root': {
                                      backgroundColor: theme.palette.primary.main,
                                  },
                              },
                          },
                      }}
                  >
                      <MenuItem value="RPIR1">RPIR1</MenuItem>
                      <MenuItem value="RPIR2">RPIR2</MenuItem>
                      <MenuItem value="RPIR3">RPIR3</MenuItem>
                      <MenuItem value="RPIR4">RPIR4</MenuItem>
                  </Select>
                  <Button variant="contained" sx={{
                      textTransform: "capitalize",
                      width: "40%"
                  }}
                          onClick={handleRpirClick}
                  >Trigger</Button>
                  
              </Box>
          </Box>


          <Box sx={{
              display: "flex",
              flexDirection: "column",
              width: "100%",
              alignItems: "center",
              gap: "10px"
          }}>
              <h2>GSG scenario</h2>
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
                          onClick={handleGsgClick}
                  >Simulate significant movement</Button>

              </Box>
          </Box>
      </Box>
  )
}