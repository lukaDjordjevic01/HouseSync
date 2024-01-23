import {Box, Button, Typography} from "@mui/material";
import {useEffect, useState} from "react";
import axios from "axios";
import {io} from "socket.io-client";

export default function BedroomAndGarage () {

    const [brgbState, setBrgbState] = useState<BrgbState>(
        {
            color: "white",
            is_on: false
        }
    )
    const [glcdData, setGlcdData] = useState<string>("");

    const palette = {
        white: "#F2F2F2",
        red: "#DD3636",
        green: "#66FF77",
        blue: "#174384",
        yellow: "#e5c507",
        lightBlue: "#4e88df",
        purple: "#522bbf",
    }

    useEffect(() => {
        axios.get<BrgbState>("http://localhost:5000/rgb-state")
            .then(res => {
                if (res.status === 200) {
                    setBrgbState(res.data);
                }
            })
            .catch(err => {
                console.log(err);
            });

        const socket = io('http://localhost:5000');
        socket.emit('subscribe', { topic: "BRGB" });
        socket.emit('subscribe', { topic: "GLCD" });

        const handleMessage = (data) => {
            if (data.topic === "BRGB") {
                setBrgbState(data.message);
            }
            if (data.topic === "GLCD") {
                setGlcdData(data.message.display_data);
            }
        }
        socket.off('message', handleMessage).on('message', handleMessage);

        return () => {
            socket.emit('unsubscribe', { topic: "BRGB" });
            socket.emit('unsubscribe', { topic: "GLCD" });
            console.log("Unmounted")
            socket.disconnect();
        };
    }, [])

    const handleButtonClick = (command: string) => {
        axios.post("http://localhost:5000/rgb-control", {command: command})
            .then(res => {
                if (res.status === 200) {
                    console.log(res);
                }
            })
            .catch(err => {
                console.log(err);
            })
    }

    return (
        <Box
            sx={{
                display: "flex",
                flexDirection: "column",
                gap: "20px",
                padding: "20px",
                width: "100%"
            }}
        >

            <Box
                sx={{
                    width: "100%"
                }}
            >
                <h1>Bedroom</h1>
                <Box
                    sx={{
                        display: "flex",
                        gap: "10px",
                        width: "100%"
                    }}
                >
                    <Box
                        sx={{
                            display: "flex",
                            flexDirection: "column",
                            gap: "5px",
                            width: "50%"
                        }}
                    >
                        <h2>Bedroom rgb</h2>
                        <Typography>Current color: {brgbState.color}, {brgbState.is_on ? "On" : "Off"}</Typography>
                        <Box>
                            <Button
                                variant="outlined"
                                sx={{
                                    marginRight: "5px",
                                    color: "#F2F2F2",
                                    borderColor: "#F2F2F2"
                                }}
                                onClick={() => handleButtonClick("on_off")}
                            >
                                {brgbState.is_on ? "Off" : "On"}
                            </Button>
                            {
                                Object.keys(palette).map((colorName) =>
                                    <Button
                                        key={colorName}
                                        sx={{
                                            backgroundColor: palette[colorName],
                                            width: "50px",
                                            height: "50px",
                                            marginRight: "5px"
                                        }}
                                        onClick={() => handleButtonClick(colorName)}
                                    />
                                )
                            }
                        </Box>
                    </Box>

                    <Box
                        sx={{
                            display: "flex",
                            flexDirection: "column",
                            gap: "5px",
                            width: "50%"
                        }}
                    >
                        <h2>Alarm clock</h2>
                    </Box>
                </Box>

            </Box>

            <Box>
                <h1>Garage</h1>
                <Box
                    sx={{
                        backgroundColor: "#4e88df",
                        width: "200px",
                        padding: "10px",
                        borderRadius: "5px",
                        border: "2px solid #F2F2F2"
                    }}
                >
                    <Typography>{glcdData}</Typography>
                </Box>
            </Box>
        </Box>
    )

}

interface BrgbState {
    color: string,
    is_on: boolean
}