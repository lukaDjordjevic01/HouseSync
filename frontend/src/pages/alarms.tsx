import {Box} from "@mui/material";
import {getGrafanaURL} from "../util/util.ts";
import {useState} from "react";
import DateTimeRangePicker from "../components/date-time-range-picker.tsx";

export default function Alarms () {

    const [timeSpanFrom, setTimeSpanFrom] = useState<string>("-1h");

    return(
        <Box
            sx={{
                width: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                height: "100%",
                justifyContent: "center",
                gap: "20px"
            }}
        >
            <Box
                sx={{
                    width: "80%"
                }}
            >
                <DateTimeRangePicker timeChangeAction={setTimeSpanFrom}/>
            </Box>
            <iframe
                src={getGrafanaURL("ALARMS", "", `now${timeSpanFrom}`)}
                width="80%"
                height="70%"
            />
        </Box>
    )
}