import { Box, Typography, Grid, Card, CardContent } from "@mui/material";

import { Activity, Bot, Brain, Workflow } from "lucide-react";

import { motion } from "framer-motion";

function DashboardCard({ title, icon, subtitle }) {
  return (
    <motion.div
      whileHover={{
        y: -4,
      }}
      transition={{
        duration: 0.25,
      }}
    >
      <Card
        sx={{
          height: "100%",
        }}
      >
        <CardContent>
          <Box display="flex" alignItems="center" gap={1.5} mb={2}>
            {icon}

            <Typography variant="h6">{title}</Typography>
          </Box>

          <Typography variant="body2">{subtitle}</Typography>
        </CardContent>
      </Card>
    </motion.div>
  );
}

function App() {
  return (
    <Box
      sx={{
        minHeight: "100vh",
        px: 4,
        py: 4,
      }}
    >
      {/* HEADER */}

      <Box mb={5}>
        <Typography variant="h3" fontWeight={700}>
          AgentOps Platform
        </Typography>

        <Typography
          variant="body1"
          sx={{
            mt: 1,
            color: "text.secondary",
          }}
        >
          Observability Dashboard · Phase 4
        </Typography>
      </Box>

      {/* DASHBOARD GRID */}

      <Grid container spacing={3}>
        <Grid item xs={12} md={6} lg={3}>
          <DashboardCard
            title="System Metrics"
            icon={<Activity size={22} />}
            subtitle="Latency, LLM and RAG statistics will appear here."
          />
        </Grid>

        <Grid item xs={12} md={6} lg={3}>
          <DashboardCard
            title="Agents"
            icon={<Bot size={22} />}
            subtitle="Agent execution analytics and routing data."
          />
        </Grid>

        <Grid item xs={12} md={6} lg={3}>
          <DashboardCard
            title="Skills"
            icon={<Brain size={22} />}
            subtitle="Skill usage and dependency execution visibility."
          />
        </Grid>

        <Grid item xs={12} md={6} lg={3}>
          <DashboardCard
            title="Execution Chains"
            icon={<Workflow size={22} />}
            subtitle="Skill chains and workflow execution traces."
          />
        </Grid>
      </Grid>
    </Box>
  );
}

export default App;
