import {Box, Button, Dialog, DialogContent, TextField, Typography, useTheme} from "@mui/material";
import DevicePopup from "./device-popup.tsx";
import React, {useState} from "react";
import axios from "axios";
import {Device} from "../model.ts";
import {toast} from "react-hot-toast";

export default function Alarm ({data}) {

    const [dialogOpen, setDialogOpen] = useState<boolean>(false);
    const [pin, setPin] = useState<string>("");
    const theme = useTheme();

    const handleOkClick = () => {
        axios.post<any>("http://localhost:5000/web-alarm-off", {id: "WEB", value: pin})
            .then(res => {
                if (res.status == 200) {
                    toast.success("Alarm turned off.", {position: "bottom-center", duration: 1});
                    setDialogOpen(false);
                }
            })
            .catch(err => {
                toast.error(err.response.data.message, {position: "bottom-center", duration: 1});
            })
    }

    return(
        <Box sx={{
            display: "flex",
            flexDirection: "column",
            gap: "20px",
            padding: "10px",
            backgroundColor: "#DD3636",
            width: "350px",
            borderRadius: "5px"
        }}>
            <Typography fontSize="large">{data.message}</Typography>
            <Button
                variant="outlined"
                sx={{
                    color: "#F2F2F2",
                    borderColor: "#F2F2F2"
                }}
                onClick={() => setDialogOpen(true)}
            >
                Turn off
            </Button>

            <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} fullWidth
                    maxWidth={"md"}>
                <DialogContent
                    sx={{
                        padding: "0",
                        width: "100%",

                    }}>
                    <Box
                        sx={{
                            backgroundColor: theme.palette.background.default,
                            color: theme.palette.primary.contrastText,
                            display: "flex",
                            gap: "10px",
                            width: "100%",
                            padding: "25px"
                        }}
                    >
                        <TextField
                            label="Pin"
                            value={pin}
                            variant="filled"
                            sx={{
                                width: "70%",
                                color: theme.palette.primary.contrastText,
                                input: {color: theme.palette.primary.contrastText}
                            }}
                            onChange={(event) => setPin(event.target.value)}
                        />
                        <Button
                            variant="contained"
                            sx={{
                                width: "30%"
                            }}
                            onClick={handleOkClick}
                        >
                            Ok
                        </Button>
                    </Box>
                </DialogContent>
            </Dialog>
        </Box>
    )
}