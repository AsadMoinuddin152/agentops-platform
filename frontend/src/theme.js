import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "dark",

    primary: {
      main: "#6C63FF",
    },

    secondary: {
      main: "#00C2FF",
    },

    background: {
      default: "#070B14",

      paper: "rgba(18, 24, 38, 0.55)",
    },

    text: {
      primary: "#F5F7FA",

      secondary: "#A7B0C0",
    },

    success: {
      main: "#22C55E",
    },

    warning: {
      main: "#F59E0B",
    },

    error: {
      main: "#EF4444",
    },
  },

  typography: {
    fontFamily: ["Inter", "sans-serif"].join(","),

    h1: {
      fontWeight: 700,
    },

    h2: {
      fontWeight: 700,
    },

    h3: {
      fontWeight: 600,
    },

    h4: {
      fontWeight: 600,
    },

    h5: {
      fontWeight: 600,
    },

    h6: {
      fontWeight: 600,
    },

    body1: {
      fontSize: "0.95rem",
    },

    body2: {
      color: "#A7B0C0",
    },
  },

  shape: {
    borderRadius: 20,
  },

  shadows: [
    "none",

    "0px 4px 20px rgba(0,0,0,0.18)",

    "0px 6px 24px rgba(0,0,0,0.22)",

    "0px 8px 28px rgba(0,0,0,0.25)",

    "0px 10px 32px rgba(0,0,0,0.28)",

    ...Array(20).fill("0px 10px 32px rgba(0,0,0,0.28)"),
  ],

  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          background: "rgba(20, 28, 45, 0.45)",

          backdropFilter: "blur(18px)",

          WebkitBackdropFilter: "blur(18px)",

          border: "1px solid rgba(255,255,255,0.08)",

          boxShadow: "0 8px 32px rgba(0,0,0,0.35)",
        },
      },
    },

    MuiPaper: {
      styleOverrides: {
        root: {
          background: "rgba(20, 28, 45, 0.45)",

          backdropFilter: "blur(18px)",

          border: "1px solid rgba(255,255,255,0.06)",
        },
      },
    },

    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 14,

          textTransform: "none",

          fontWeight: 600,
        },
      },
    },
  },
});

export default theme;
