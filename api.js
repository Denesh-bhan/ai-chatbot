import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const api = axios.create({ baseURL: API, timeout: 20000 });

export async function fetchLibrary() {
  const { data } = await api.get("/library");
  return data;
}

export async function fetchPrompts() {
  const { data } = await api.get("/prompts");
  return data;
}

export async function sendChat({ query, sessionId }) {
  const { data } = await api.post("/chat", { query, session_id: sessionId });
  return data;
}

export async function seedDatabase() {
  const { data } = await api.post("/seed");
  return data;
}

// Admin helpers - use these to add more data
export async function addDocument(doc) {
  const { data } = await api.post("/documents", doc);
  return data;
}
export async function addPrompt(p) {
  const { data } = await api.post("/prompts", p);
  return data;
}
export async function addAnswer(a) {
  const { data } = await api.post("/answers", a);
  return data;
}
export async function addStat(s) {
  const { data } = await api.post("/stats", s);
  return data;
}
