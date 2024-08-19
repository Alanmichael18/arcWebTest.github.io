import React from "react";
import ReactDOM from "react-dom/client";
// import App from "./App.tsx";
import Menu from "./pages/Menu.tsx";
import "./index.css";
import {ErrorBoundary} from "@highlight-run/react";
import {H} from "highlight.run";

H.init("lgxy4pdm", {
    serviceName: "frontend-app",
    tracingOrigins: [
        'python-flask-backend.onrender.com',
        'localhost',
        'localhost:5001',
    ],
    privacySetting: 'none',
    networkRecording: {
        enabled: true,
        recordHeadersAndBody: true,
    },
});

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <ErrorBoundary>
            <Menu/>
        </ErrorBoundary>
    </React.StrictMode>,
);