import ReactDOM from 'react-dom/client'
import './index.css'
import {createTheme, CssBaseline, ThemeProvider} from "@mui/material";
import {RouterProvider, createBrowserRouter} from "react-router-dom";
import Navbar from "./components/navbar.tsx";
import Alarms from "./pages/alarms.tsx";
import Devices from "./pages/devices.tsx";

const theme = createTheme({
    palette: {
        primary: {
            main: "#4D4D4D",
            light: "#174384",
            contrastText: "#F2F2F2"
        },
        secondary: {
            main: "#F5F5F5",
            contrastText: '#4D4D4D'
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
            {path: "/alarms", element: <Alarms/>},
            {path: "/devices", element: <Devices/>}
        ]
    }
])

ReactDOM.createRoot(document.getElementById('root')!).render(
    <ThemeProvider theme={theme} >
        <CssBaseline/>
        <RouterProvider router={router}/>
    </ThemeProvider>
)
