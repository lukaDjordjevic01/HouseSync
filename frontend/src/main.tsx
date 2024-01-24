import ReactDOM from 'react-dom/client'
import './index.css'
import {createTheme, CssBaseline, ThemeProvider} from "@mui/material";
import {RouterProvider, createBrowserRouter} from "react-router-dom";
import Navbar from "./components/navbar.tsx";
import Alarms from "./pages/alarms.tsx";
import Devices from "./pages/devices.tsx";
import Scenarios from "./pages/scenarios.tsx";
import {toast, Toaster} from "react-hot-toast";
import {io} from "socket.io-client";
import {Howl} from 'howler';
import Alarm from "./components/alarm.tsx";
import BedroomAndGarage from "./pages/bedroom-and-garage.tsx";
import {LocalizationProvider} from "@mui/x-date-pickers";
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import AlarmClock from "./components/alarm-clock.tsx";

const theme = createTheme({
    palette: {
        primary: {
            main: "#4D4D4D",
            light: "#174384",
            contrastText: "#F2F2F2"
        },
        secondary: {
            main: '#F2F2F2',
            contrastText: "#F2F2F2"
        },
        error: {
            main: "#DD3636"
        },
        success: {
            main: "#66FF77"
        },
        background: {
            default: "#1E1E1E",
        }
    },
    typography: {
        allVariants: {
            color: "#F2F2F2",
            fontFamily: "Poppins"
        },

    },
});

const router = createBrowserRouter([
    {
        path:"/",
        element: <Navbar/>,
        children:[
            {path:"/", element: <Devices/>},
            {path: "/alarms", element: <Alarms/>},
            {path: "/devices", element: <Devices/>},
            {path: "/scenarios", element: <Scenarios/>},
            {path: "/bedroom-and-garage", element: <BedroomAndGarage/>},
        ]
    }
])

const socket = io('http://localhost:5000');
socket.emit('subscribe', { topic: "Alarm" });
socket.emit('subscribe', { topic: "Alarm-clock" });

const handleAlarm = (data) => {

    if (data.topic == "Alarm") {
        const howl = new Howl({
            src: ["src/assets/alarm_beep.mp3"]
        });
        howl.play();
        toast.custom(
            <Alarm data={data}/>
        )
    }
    if (data.topic == "Alarm-clock") {
        const howl = new Howl({
            src: ["src/assets/alarm-clock.mp3"]
        });
        howl.play();
        toast.custom(
            <AlarmClock/>
        )
    }

}
socket.off('message', handleAlarm).on('message', handleAlarm);


ReactDOM.createRoot(document.getElementById('root')!).render(
    <ThemeProvider theme={theme} >
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <CssBaseline/>
            <RouterProvider router={router}/>
            <Toaster position="bottom-right"/>
        </LocalizationProvider>
    </ThemeProvider>
)
