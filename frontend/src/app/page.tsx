'use client';

import { useMemo, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Grid,
  List,
  ListItem,
  ListItemText,
  Stack,
  TextField,
  Typography,
} from '@mui/material';

const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000';

type SignalResponse = {
  signal: string;
  uses: string[];
  used_by: string[];
  related_calibrations: string[];
};

export default function Home() {
  const [token, setToken] = useState<string>('');
  const [username, setUsername] = useState('engineer');
  const [password, setPassword] = useState('calai');
  const [uploadResult, setUploadResult] = useState('');
  const [chatQuestion, setChatQuestion] = useState('What enables DTC P0087?');
  const [chatAnswer, setChatAnswer] = useState('');
  const [signal, setSignal] = useState('LPSys_pSet');
  const [signalData, setSignalData] = useState<SignalResponse | null>(null);
  const [diagCode, setDiagCode] = useState('P0087');
  const [diagData, setDiagData] = useState<Record<string, unknown> | null>(null);
  const [message, setMessage] = useState<string>('');

  const authHeader = useMemo(
    () => (token ? { Authorization: 'Bearer ' + token } : {}),
    [token],
  );

  const login = async () => {
    const res = await fetch(`${apiBase}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) {
      setMessage('Login failed');
      return;
    }
    const data = await res.json();
    setToken(data.access_token);
    setMessage('Login successful');
  };

  const uploadFile = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const body = new FormData();
    body.append('file', file);
    const res = await fetch(`${apiBase}/api/documents/upload`, {
      method: 'POST',
      body,
      headers: authHeader,
    });

    if (!res.ok) {
      setUploadResult('Upload failed');
      return;
    }

    const data = await res.json();
    setUploadResult(`Indexed ${data.filename} (${data.bytes} bytes)`);
  };

  const ask = async () => {
    const res = await fetch(`${apiBase}/api/chat/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...authHeader },
      body: JSON.stringify({ question: chatQuestion }),
    });
    if (!res.ok) {
      setChatAnswer('Unable to get answer');
      return;
    }
    const data = await res.json();
    setChatAnswer(`${data.answer}\n\nConfidence: ${data.confidence}`);
  };

  const loadSignal = async () => {
    const res = await fetch(`${apiBase}/api/signals/${encodeURIComponent(signal)}/dependencies`);
    if (!res.ok) return;
    setSignalData(await res.json());
  };

  const loadDiagnostic = async () => {
    const res = await fetch(`${apiBase}/api/diagnostics/${encodeURIComponent(diagCode)}`);
    if (!res.ok) return;
    setDiagData(await res.json());
  };

  return (
    <Container sx={{ py: 4 }}>
      <Stack spacing={3}>
        <Typography variant="h4">CalAI MVP</Typography>
        <Typography>
          Self-hosted calibration and diagnostics intelligence workflow with authentication, upload, RAG-style chat,
          signal dependency lookup, and diagnostic exploration.
        </Typography>
        {message && <Alert severity="info">{message}</Alert>}

        <Grid container spacing={2}>
          <Grid size={{ xs: 12, md: 6 }}>
            <Card>
              <CardContent>
                <Typography variant="h6">Authentication</Typography>
                <Stack spacing={1} sx={{ mt: 1 }}>
                  <TextField label="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
                  <TextField
                    label="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                  <Button variant="contained" onClick={login}>
                    Login
                  </Button>
                  <Typography variant="body2">Token: {token ? `${token.slice(0, 16)}...` : 'Not logged in'}</Typography>
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <Card>
              <CardContent>
                <Typography variant="h6">Document Upload</Typography>
                <Stack spacing={1} sx={{ mt: 1 }}>
                  <Button component="label" variant="outlined">
                    Select File
                    <input hidden type="file" onChange={uploadFile} />
                  </Button>
                  <Typography variant="body2">{uploadResult || 'No file uploaded yet'}</Typography>
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <Card>
              <CardContent>
                <Typography variant="h6">AI Engineering Chat</Typography>
                <Stack spacing={1} sx={{ mt: 1 }}>
                  <TextField
                    multiline
                    minRows={2}
                    label="Question"
                    value={chatQuestion}
                    onChange={(e) => setChatQuestion(e.target.value)}
                  />
                  <Button variant="contained" onClick={ask}>
                    Ask
                  </Button>
                  <Typography sx={{ whiteSpace: 'pre-wrap' }}>{chatAnswer || 'Answer will appear here.'}</Typography>
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <Card>
              <CardContent>
                <Typography variant="h6">Signal Dependency Explorer</Typography>
                <Stack spacing={1} sx={{ mt: 1 }}>
                  <TextField label="Signal" value={signal} onChange={(e) => setSignal(e.target.value)} />
                  <Button variant="contained" onClick={loadSignal}>
                    Load Dependencies
                  </Button>
                  {signalData && (
                    <Box>
                      <Typography variant="subtitle2">Uses</Typography>
                      <List dense>
                        {signalData.uses.map((item) => (
                          <ListItem key={item}>
                            <ListItemText primary={item} />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  )}
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12 }}>
            <Card>
              <CardContent>
                <Typography variant="h6">Diagnostic Explorer</Typography>
                <Stack direction={{ xs: 'column', md: 'row' }} spacing={1} sx={{ mt: 1 }}>
                  <TextField label="DTC" value={diagCode} onChange={(e) => setDiagCode(e.target.value)} />
                  <Button variant="contained" onClick={loadDiagnostic}>
                    Load DTC Context
                  </Button>
                </Stack>
                {diagData && (
                  <Box sx={{ mt: 2 }}>
                    <Typography component="pre" sx={{ whiteSpace: 'pre-wrap', m: 0 }}>
                      {JSON.stringify(diagData, null, 2)}
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Stack>
    </Container>
  );
}
