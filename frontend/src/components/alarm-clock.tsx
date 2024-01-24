import {Box, Button, Typography} from "@mui/material";
import React from "react";
import axios from "axios";

export default function AlarmClock() {

    const handleTurnOff = () => {
        axios.post("http://localhost:5000/alarm-clock", {command: "turn_off"})
            .then(res => {
                if (res.status === 200) {
                    console.log(res);
                }
            })
            .catch(err => {
                console.log(err);
            })
    }

    return(
        <Box sx={{
            display: "flex",
            flexDirection: "column",
            gap: "20px",
            padding: "10px",
            backgroundColor: "#174384",
            width: "350px",
            borderRadius: "5px"
        }}>
            <Typography fontSize="large">Alarm clock is triggered</Typography>
            <Button
                variant="outlined"
                sx={{
                    color: "#F2F2F2",
                    borderColor: "#F2F2F2"
                }}
                onClick={handleTurnOff}
            >
                Turn off
            </Button>
        </Box>
    )
}