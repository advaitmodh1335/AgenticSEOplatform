"use client";

import { useEffect, useState } from "react";
import {
  checkHealth,
  createProject,
  getProjects,
  createCompetitor,
  scrapeCompetitor,
} from "@/lib/api";

type Project = {
  id: number;
  name: string;
  niche: string;
  target_audience: string;
  seed_keywords: string[];
};

export default function Home() {
  const [healthStatus, setHealthStatus] = useState("Checking...");
  const [projects, setProjects] = useState<Project[]>([]);

  const [projectName, setProjectName] = useState("");
  const [niche, setNiche] = useState("");
  const [targetAudience, setTargetAudience] = useState("");
  const [seedKeywords, setSeedKeywords] = useState("");

  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [competitorName, setCompetitorName] = useState("");
  const [competitorUrl, setCompetitorUrl] = useState("");

  const [scrapeResult, setScrapeResult] = useState<any>(null);

  async function loadProjects() {
    try {
      const data = await getProjects();
      setProjects(data);
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    async function fetchHealth() {
      try {
        const data = await checkHealth();
        setHealthStatus(data.status);
      } catch {
        setHealthStatus("Backend not reachable");
      }
    }

    fetchHealth();
    loadProjects();
  }, []);

  async function handleCreateProject(e: React.FormEvent) {
    e.preventDefault();

    try {
      await createProject({
        name: projectName,
        niche,
        target_audience: targetAudience,
        seed_keywords: seedKeywords
          .split(",")
          .map((keyword) => keyword.trim())
          .filter(Boolean),
      });

      setProjectName("");
      setNiche("");
      setTargetAudience("");
      setSeedKeywords("");
      await loadProjects();
    } catch (error) {
      console.error(error);
      alert("Failed to create project");
    }
  }

  async function handleCreateCompetitor(e: React.FormEvent) {
    e.preventDefault();

    try {
      await createCompetitor({
        project_id: Number(selectedProjectId),
        name: competitorName,
        url: competitorUrl,
      });

      setCompetitorName("");
      setCompetitorUrl("");
      alert("Competitor added successfully");
    } catch (error) {
      console.error(error);
      alert("Failed to add competitor");
    }
  }

  async function handleScrapeCompetitor() {
    try {
      const data = await scrapeCompetitor(competitorUrl);
      setScrapeResult(data);
    } catch (error) {
      console.error(error);
      alert("Failed to scrape competitor");
    }
  }

  return (
    <main className="min-h-screen p-8 max-w-4xl mx-auto space-y-10">
      <section>
        <h1 className="text-3xl font-bold mb-2">Agentic SEO Platform</h1>
        <p className="text-gray-600">Backend health: {healthStatus}</p>
      </section>

      <section className="border rounded-xl p-6 space-y-4">
        <h2 className="text-2xl font-semibold">Create Project</h2>
        <form onSubmit={handleCreateProject} className="space-y-4">
          <input
            className="w-full border rounded-lg p-3"
            placeholder="Project Name"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
          />
          <input
            className="w-full border rounded-lg p-3"
            placeholder="Niche"
            value={niche}
            onChange={(e) => setNiche(e.target.value)}
          />
          <input
            className="w-full border rounded-lg p-3"
            placeholder="Target Audience"
            value={targetAudience}
            onChange={(e) => setTargetAudience(e.target.value)}
          />
          <input
            className="w-full border rounded-lg p-3"
            placeholder="Seed Keywords (comma separated)"
            value={seedKeywords}
            onChange={(e) => setSeedKeywords(e.target.value)}
          />
          <button className="bg-black text-white px-5 py-3 rounded-lg">
            Create Project
          </button>
        </form>
      </section>

      <section className="border rounded-xl p-6 space-y-4">
        <h2 className="text-2xl font-semibold">Projects</h2>
        {projects.length === 0 ? (
          <p className="text-gray-600">No projects created yet.</p>
        ) : (
          <ul className="space-y-3">
            {projects.map((project) => (
              <li key={project.id} className="border rounded-lg p-4">
                <p><strong>Name:</strong> {project.name}</p>
                <p><strong>Niche:</strong> {project.niche}</p>
                <p><strong>Audience:</strong> {project.target_audience}</p>
                <p><strong>Keywords:</strong> {project.seed_keywords.join(", ")}</p>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="border rounded-xl p-6 space-y-4">
        <h2 className="text-2xl font-semibold">Add Competitor</h2>
        <form onSubmit={handleCreateCompetitor} className="space-y-4">
          <select
            className="w-full border rounded-lg p-3"
            value={selectedProjectId}
            onChange={(e) => setSelectedProjectId(e.target.value)}
          >
            <option value="">Select Project</option>
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.name}
              </option>
            ))}
          </select>

          <input
            className="w-full border rounded-lg p-3"
            placeholder="Competitor Name"
            value={competitorName}
            onChange={(e) => setCompetitorName(e.target.value)}
          />

          <input
            className="w-full border rounded-lg p-3"
            placeholder="Competitor Blog URL"
            value={competitorUrl}
            onChange={(e) => setCompetitorUrl(e.target.value)}
          />

          <div className="flex gap-3">
            <button className="bg-black text-white px-5 py-3 rounded-lg">
              Add Competitor
            </button>

            <button
              type="button"
              onClick={handleScrapeCompetitor}
              className="bg-blue-600 text-white px-5 py-3 rounded-lg"
            >
              Test Scrape
            </button>
          </div>
        </form>

        {scrapeResult && (
          <div className="border rounded-lg p-4 mt-4 space-y-3">
            <h3 className="text-xl font-semibold">Scrape Result</h3>

            <p>
              <strong>Title:</strong> {scrapeResult.title}
            </p>

            <p>
              <strong>Meta Description:</strong> {scrapeResult.meta_description}
            </p>

            <div>
              <strong>Headings:</strong>
              <ul className="list-disc ml-6">
                {scrapeResult.headings.map((heading: string, index: number) => (
                  <li key={index}>{heading}</li>
                ))}
              </ul>
            </div>

            <div>
              <strong>Content Preview:</strong>
              <ul className="list-disc ml-6">
                {scrapeResult.content_preview.map((paragraph: string, index: number) => (
                  <li key={index}>{paragraph}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </section>
    </main>
  );
}