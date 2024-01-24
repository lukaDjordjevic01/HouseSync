import {Box, Button, Typography, useTheme} from "@mui/material";
import {useEffect, useState} from "react";
import axios from "axios";
import {io} from "socket.io-client";
import {TimePicker} from "@mui/x-date-pickers";
import dayjs, { Dayjs } from 'dayjs';

export default function BedroomAndGarage () {

    const [brgbState, setBrgbState] = useState<BrgbState>(
        {
            color: "white",
            is_on: false
        }
    )
    const [glcdData, setGlcdData] = useState<string>("");

    const [b4sdTime, setB4sdTime] = useState<string>("");
    const [alarmClockTime, setAlarmClockTime] = useState<Dayjs | null>(dayjs());
    const [alarmClockState, setAlarmClockState] = useState<AlarmClockState>(
        {
            time: "",
            system_is_on: false
        }
    )

    const theme = useTheme();

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

        axios.get("http://localhost:5000/get-time")
            .then(res => {
                if (res.status === 200) {
                    setB4sdTime(res.data.time);
                }
            })
            .catch(err => {
                console.log(err);
            });

        axios.get<AlarmClockState>("http://localhost:5000/get-alarm-clock")
            .then(res => {
                if (res.status === 200) {
                    setAlarmClockState(res.data);
                }
            })
            .catch(err => {
                console.log(err);
            });

        const socket = io('http://localhost:5000');
        socket.emit('subscribe', { topic: "BRGB" });
        socket.emit('subscribe', { topic: "GLCD" });
        socket.emit('subscribe', { topic: "B4SD" });

        const handleMessage = (data) => {
            if (data.topic === "BRGB") {
                setBrgbState(data.message);
            }
            if (data.topic === "GLCD") {
                setGlcdData(data.message.display_data);
            }
            if (data.topic === "B4SD") {
                setB4sdTime(data.message.time)
            }
        }
        socket.off('message', handleMessage).on('message', handleMessage);

        return () => {
            socket.emit('unsubscribe', { topic: "BRGB" });
            socket.emit('unsubscribe', { topic: "GLCD" });
            socket.emit('unsubscribe', { topic: "B4SD" });
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

    const handleAlarmOnOffClick = (command: string) => {
        axios.post("http://localhost:5000/alarm-clock", {command: command, is_on: !alarmClockState.system_is_on})
            .then(res => {
                if (res.status === 200) {
                    setAlarmClockState(res.data);
                }
            })
            .catch(err => {
                console.log(err);
            })
    }

    const handleAlarmSetClick = (command: string) => {
        axios.post("http://localhost:5000/alarm-clock",
                {
                    command: command,
                    alarm_clock_timestamp: alarmClockTime.valueOf()
                })
            .then(res => {
                if (res.status === 200) {
                    setAlarmClockState(res.data);
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
                        <Box
                            sx={{
                                display: "flex",
                                gap: "30px",
                                width: "100%",

                            }}
                        >
                            <Box>
                                <Typography>Bedroom 4SD</Typography>
                                <Box
                                    sx={{
                                        display: "flex",
                                        justifyContent: "center",
                                        backgroundColor: "black",
                                        width: "70px",
                                        padding: "10px",
                                        borderRadius: "5px",
                                        border: "2px solid #4D4D4D",
                                        marginTop: "10px"
                                    }}
                                >
                                    <Typography
                                        sx={{
                                            color: "#DD3636"
                                        }}
                                    >
                                        {b4sdTime}
                                    </Typography>
                                </Box>
                            </Box>

                            <Box>
                                <Typography>
                                    Current settings: {alarmClockState.time}, {alarmClockState.system_is_on ? "On" : "Off"}
                                </Typography>

                                <Box
                                    sx={{
                                        marginTop: "10px",
                                        display: "flex",
                                        gap: "10px",
                                    }}
                                >
                                    <Button
                                        variant="outlined"
                                        sx={{
                                            color: "#F2F2F2",
                                            borderColor: "#F2F2F2"
                                        }}
                                        onClick={() => handleAlarmOnOffClick("system")}
                                    >
                                        {alarmClockState.system_is_on ? "Off" : "On"}
                                    </Button>

                                    <TimePicker
                                        label="Start"
                                        ampm={false}
                                        value={alarmClockTime}
                                        onChange={(newValue) => setAlarmClockTime(newValue)}
                                        sx={{
                                            width: "120px",
                                            color: "#F2F2F2",
                                            borderColor: "#F2F2F2",
                                            input: {
                                                color: "#F2F2F2",
                                            },
                                            outlineColor: "secondary"
                                        }}
                                        slotProps={{
                                            openPickerButton: {
                                              color: "secondary"
                                            },
                                            digitalClockSectionItem: {
                                                sx: {
                                                    backgroundColor: theme.palette.background.default,
                                                    "&:hover": {
                                                        backgroundColor: "#4D4D4D"
                                                    }
                                                },
                                            },
                                        }}
                                    />

                                    <Button
                                        variant="outlined"
                                        sx={{
                                            marginRight: "5px",
                                            color: "#F2F2F2",
                                            borderColor: "#F2F2F2"
                                        }}
                                        onClick={() => handleAlarmSetClick("setup")}
                                    >
                                        Set
                                    </Button>

                                </Box>

                            </Box>

                        </Box>

                    </Box>
                </Box>

            </Box>

            <Box>
                <h1>Garage</h1>

                <Box>
                    <h2>Garage lcd</h2>
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
        </Box>
    )

}

interface BrgbState {
    color: string,
    is_on: boolean
}

interface AlarmClockState {
    time: string,
    system_is_on: boolean
}