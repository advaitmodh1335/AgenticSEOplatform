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

export async function scrapeCompetitor(
  url: string,
  project_id: number,
  competitor_id?: number
) {
  const response = await fetch(`${API_BASE_URL}/competitors/scrape`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url, project_id, competitor_id }),
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

export async function getCompetitors(projectId?: number) {
  const url = projectId
    ? `${API_BASE_URL}/competitors/project/${projectId}`
    : `${API_BASE_URL}/competitors`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch competitors");
  }

  return response.json();
}

export async function createDocument(data: {
  project_id: number;
  title: string;
  doc_type: string;
  content: string;
}) {
  const response = await fetch(`${API_BASE_URL}/documents`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Failed to create document");
  }

  return response.json();
}

export async function getDocuments() {
  const response = await fetch(`${API_BASE_URL}/documents`);

  if (!response.ok) {
    throw new Error("Failed to fetch documents");
  }

  return response.json();
}

export async function buildRagIndex(project_id: number) {
  const response = await fetch(`${API_BASE_URL}/rag/index`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ project_id }),
  });

  if (!response.ok) {
    throw new Error("Failed to build RAG index");
  }

  return response.json();
}

export async function queryRag(data: { query: string; top_k?: number }) {
  const response = await fetch(`${API_BASE_URL}/rag/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Failed to query RAG");
  }

  return response.json();
}

export async function getTopicSuggestions(project_id: number) {
  const response = await fetch(`${API_BASE_URL}/strategy/topics`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ project_id }),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch topic suggestions");
  }

  return response.json();
}

export async function generateOutline(data: {
  project_id: number;
  topic: string;
  keyword: string;
}) {
  const response = await fetch(`${API_BASE_URL}/content/outline`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Failed to generate outline");
  }

  return response.json();
}