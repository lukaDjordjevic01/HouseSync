import {Box, Button, Dialog, DialogContent, MenuItem, Select, useTheme} from "@mui/material";
import React, {useEffect, useState} from "react";

export default function DateTimeRangePicker({timeChangeAction})  {

    const [timespanFrom, setTimespan] = useState<string>("-1h")
    const theme = useTheme();

    useEffect(() => {
        timeChangeAction(timespanFrom);
    }, [timespanFrom])

    return (
        <>
            <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                label="Timespan"
                value={timespanFrom}
                onChange={(e) => setTimespan(e.target.value as string)}
                sx={{
                    width: "20%",
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
                <MenuItem value="-1h">🕒 Past 1h</MenuItem>
                <MenuItem value="-6h">🕒 Past 6h</MenuItem>
                <MenuItem value="-12h">🕒 Past 12h</MenuItem>
                <MenuItem value="-24h">🕒 Past 24h</MenuItem>
                <MenuItem value="-168h">🕒 Past week</MenuItem>
                <MenuItem value="-720h">🕒 Past month</MenuItem>
            </Select>

        </>
    )
}