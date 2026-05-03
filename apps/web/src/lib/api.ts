const API_BASE_URL = "http://127.0.0.1:8000";

export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) throw new Error("Failed to fetch health status");
  return response.json();
}

export async function createProject(data: {
  name: string;
  niche: string;
  target_audience: string;
  seed_keywords: string[];
}) {
  const response = await fetch(`${API_BASE_URL}/projects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) throw new Error("Failed to create project");
  return response.json();
}

export async function getProjects() {
  const response = await fetch(`${API_BASE_URL}/projects`);
  if (!response.ok) throw new Error("Failed to fetch projects");
  return response.json();
}

export async function createCompetitor(data: {
  project_id: number;
  name: string;
  url: string;
}) {
  const response = await fetch(`${API_BASE_URL}/competitors`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) throw new Error("Failed to create competitor");
  return response.json();
}

export async function scrapeCompetitor(url: string, competitor_id?: number) {
  const response = await fetch(`${API_BASE_URL}/competitors/scrape`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url, competitor_id }),
  });

  if (!response.ok) {
    throw new Error("Failed to scrape competitor URL");
  }

  return response.json();
}

export async function getScrapes() {
  const response = await fetch(`${API_BASE_URL}/competitors/scrapes`);

  if (!response.ok) {
    throw new Error("Failed to fetch scrape history");
  }

  return response.json();
}