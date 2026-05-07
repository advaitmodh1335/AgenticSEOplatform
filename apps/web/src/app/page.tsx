"use client";

import { useEffect, useState } from "react";
import {
  checkHealth,
  createProject,
  getProjects,
  createCompetitor,
  scrapeCompetitor,
  getScrapes,
  getCompetitors,
  createDocument,
  getDocuments,
  buildRagIndex,
  queryRag,
  getTopicSuggestions,
  generateOutline,
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
  const [scrapeHistory, setScrapeHistory] = useState<any[]>([]);

  const [competitors, setCompetitors] = useState<any[]>([]);

  const [documents, setDocuments] = useState<any[]>([]);
  const [documentTitle, setDocumentTitle] = useState("");
  const [documentType, setDocumentType] = useState("style_guide");
  const [documentContent, setDocumentContent] = useState("");
  const [documentProjectId, setDocumentProjectId] = useState("");

  const [ragProjectId, setRagProjectId] = useState("");
  const [ragQuery, setRagQuery] = useState("");
  const [ragResults, setRagResults] = useState<any[]>([]);

  const [topicProjectId, setTopicProjectId] = useState("");
  const [topicSuggestions, setTopicSuggestions] = useState<any[]>([]);

  const [outlineProjectId, setOutlineProjectId] = useState("");
  const [outlineTopic, setOutlineTopic] = useState("");
  const [outlineKeyword, setOutlineKeyword] = useState("");
  const [generatedOutline, setGeneratedOutline] = useState<any>(null);

  async function loadProjects() {
    try {
      const data = await getProjects();
      setProjects(data);
    } catch (error) {
      console.error(error);
    }
  }

  async function loadScrapes() {
    try {
      const data = await getScrapes();
      setScrapeHistory(data);
    } catch (error) {
      console.error(error);
    }
  }

  async function loadCompetitors(projectId?: number) {
    try {
      const data = await getCompetitors(projectId);
      setCompetitors(data);
    } catch (error) {
      console.error(error);
    }
  }

  async function loadDocuments() {
    try {
      const data = await getDocuments();
      setDocuments(data);
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
    loadScrapes();
    loadCompetitors();
    loadDocuments();
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
      await loadCompetitors();
      alert("Competitor added successfully");
    } catch (error) {
      console.error(error);
      alert("Failed to add competitor");
    }
  }

  async function handleScrapeCompetitor() {
    try {
      if (!selectedProjectId) {
        alert("Please select a project before scraping");
        return;
      }

      const data = await scrapeCompetitor(
        competitorUrl,
        Number(selectedProjectId)
      );

      setScrapeResult(data);
      await loadScrapes();
    } catch (error) {
      console.error(error);
      alert("Failed to scrape competitor");
    }
  }

  async function handleCreateDocument(e: React.FormEvent) {
    e.preventDefault();

    try {
      await createDocument({
        project_id: Number(documentProjectId),
        title: documentTitle,
        doc_type: documentType,
        content: documentContent,
      });

      setDocumentTitle("");
      setDocumentType("style_guide");
      setDocumentContent("");
      setDocumentProjectId("");
      await loadDocuments();
      alert("Document added successfully");
    } catch (error) {
      console.error(error);
      alert("Failed to add document");
    }
  }

  async function handleBuildIndex() {
    try {
      const result = await buildRagIndex(Number(ragProjectId));
      alert(`RAG index built successfully with ${result.count} chunks`);
    } catch (error) {
      console.error(error);
      alert("Failed to build RAG index");
    }
  }

  async function handleQueryRag() {
    try {
      const result = await queryRag({
        query: ragQuery,
        top_k: 5,
      });
      setRagResults(result.results || []);
    } catch (error) {
      console.error(error);
      alert("Failed to query RAG");
    }
  }

  async function handleGetTopicSuggestions() {
    try {
      const result = await getTopicSuggestions(Number(topicProjectId));
      setTopicSuggestions(result.topics || []);
    } catch (error) {
      console.error(error);
      alert("Failed to get topic suggestions");
    }
  }

  async function handleGenerateOutline() {
    try {
      const result = await generateOutline({
        project_id: Number(outlineProjectId),
        topic: outlineTopic,
        keyword: outlineKeyword,
      });

      setGeneratedOutline(result.outline);
    } catch (error) {
      console.error(error);
      alert("Failed to generate outline");
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
        <h2 className="text-2xl font-semibold">Saved Competitors</h2>

        {competitors.length === 0 ? (
          <p className="text-gray-600">No competitors added yet.</p>
        ) : (
          <ul className="space-y-3">
            {competitors.map((competitor) => (
              <li key={competitor.id} className="border rounded-lg p-4">
                <p><strong>Name:</strong> {competitor.name}</p>
                <p><strong>URL:</strong> {competitor.url}</p>
                <p><strong>Project ID:</strong> {competitor.project_id}</p>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="border rounded-xl p-6 space-y-4">
        <h2 className="text-2xl font-semibold">Knowledge Base Documents</h2>

        <form onSubmit={handleCreateDocument} className="space-y-4">
          <select
            className="w-full border rounded-lg p-3"
            value={documentProjectId}
            onChange={(e) => setDocumentProjectId(e.target.value)}
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
            placeholder="Document Title"
            value={documentTitle}
            onChange={(e) => setDocumentTitle(e.target.value)}
          />

          <select
            className="w-full border rounded-lg p-3"
            value={documentType}
            onChange={(e) => setDocumentType(e.target.value)}
          >
            <option value="style_guide">Style Guide</option>
            <option value="seo_guidelines">SEO Guidelines</option>
            <option value="past_blog">Past Blog</option>
            <option value="product_info">Product Info</option>
          </select>

          <textarea
            className="w-full border rounded-lg p-3 min-h-[160px]"
            placeholder="Paste document content here"
            value={documentContent}
            onChange={(e) => setDocumentContent(e.target.value)}
          />

          <button className="bg-black text-white px-5 py-3 rounded-lg">
            Add Document
          </button>
        </form>

        {documents.length > 0 && (
          <div className="space-y-3">
            <h3 className="text-xl font-semibold">Saved Documents</h3>
            <ul className="space-y-3">
              {documents.map((doc) => (
                <li key={doc.id} className="border rounded-lg p-4">
                  <p><strong>Title:</strong> {doc.title}</p>
                  <p><strong>Type:</strong> {doc.doc_type}</p>
                  <p><strong>Project ID:</strong> {doc.project_id}</p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>

      <section className="border rounded-xl p-6 space-y-4">
        <h2 className="text-2xl font-semibold">RAG Testing</h2>

        <select
          className="w-full border rounded-lg p-3"
          value={ragProjectId}
          onChange={(e) => setRagProjectId(e.target.value)}
        >
          <option value="">Select Project</option>
          {projects.map((project) => (
            <option key={project.id} value={project.id}>
              {project.name}
            </option>
          ))}
        </select>

        <button
          type="button"
          onClick={handleBuildIndex}
          className="bg-black text-white px-5 py-3 rounded-lg"
        >
          Build RAG Index
        </button>

        <input
          className="w-full border rounded-lg p-3"
          placeholder="Ask a question about your content"
          value={ragQuery}
          onChange={(e) => setRagQuery(e.target.value)}
        />

        <button
          type="button"
          onClick={handleQueryRag}
          className="bg-blue-600 text-white px-5 py-3 rounded-lg"
        >
          Query RAG
        </button>

        {ragResults.length > 0 && (
          <div className="space-y-3">
            <h3 className="text-xl font-semibold">Retrieved Chunks</h3>
            {ragResults.map((result, index) => (
              <div key={index} className="border rounded-lg p-4">
                <p><strong>Title:</strong> {result.title}</p>
                <p><strong>Source Type:</strong> {result.source_type}</p>
                <p><strong>Text:</strong> {result.text}</p>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="border rounded-xl p-6 space-y-4">
        <h2 className="text-2xl font-semibold">Topic Suggestions</h2>

        <select
          className="w-full border rounded-lg p-3"
          value={topicProjectId}
          onChange={(e) => setTopicProjectId(e.target.value)}
        >
          <option value="">Select Project</option>
          {projects.map((project) => (
            <option key={project.id} value={project.id}>
              {project.name}
            </option>
          ))}
        </select>

        <button
          type="button"
          onClick={handleGetTopicSuggestions}
          className="bg-black text-white px-5 py-3 rounded-lg"
        >
          Generate Topic Suggestions
        </button>

        {topicSuggestions.length > 0 && (
          <div className="space-y-3">
            <h3 className="text-xl font-semibold">Suggested Topics</h3>
            <ul className="space-y-3">
              {topicSuggestions.map((topic, index) => (
                <li key={index} className="border rounded-lg p-4">
                  <p><strong>Title:</strong> {topic.title}</p>
                  <p><strong>Keyword:</strong> {topic.keyword}</p>
                  <p><strong>Reason:</strong> {topic.reason}</p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>

      <section className="border rounded-xl p-6 space-y-4">
        <h2 className="text-2xl font-semibold">Blog Outline Generation</h2>

        <select
          className="w-full border rounded-lg p-3"
          value={outlineProjectId}
          onChange={(e) => setOutlineProjectId(e.target.value)}
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
          placeholder="Topic"
          value={outlineTopic}
          onChange={(e) => setOutlineTopic(e.target.value)}
        />

        <input
          className="w-full border rounded-lg p-3"
          placeholder="Primary Keyword"
          value={outlineKeyword}
          onChange={(e) => setOutlineKeyword(e.target.value)}
        />

        <button
          type="button"
          onClick={handleGenerateOutline}
          className="bg-black text-white px-5 py-3 rounded-lg"
        >
          Generate Blog Outline
        </button>

        {generatedOutline && (
          <div className="border rounded-lg p-4 space-y-4">
            <h3 className="text-xl font-semibold">Generated Outline</h3>

            <p><strong>Title:</strong> {generatedOutline.title}</p>
            <p><strong>Meta Title:</strong> {generatedOutline.meta_title}</p>
            <p><strong>Meta Description:</strong> {generatedOutline.meta_description}</p>
            <p><strong>Intro:</strong> {generatedOutline.intro}</p>

            <div>
              <strong>Sections:</strong>
              <ul className="list-disc ml-6">
                {generatedOutline.sections.map((section: string, index: number) => (
                  <li key={index}>{section}</li>
                ))}
              </ul>
            </div>

            <div>
              <strong>FAQ:</strong>
              <ul className="list-disc ml-6">
                {generatedOutline.faq.map((item: string, index: number) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

            <p><strong>CTA:</strong> {generatedOutline.cta}</p>

            {generatedOutline.retrieved_context?.length > 0 && (
              <div>
                <strong>Retrieved Context Used:</strong>
                <ul className="space-y-2 mt-2">
                  {generatedOutline.retrieved_context.map((chunk: any, index: number) => (
                    <li key={index} className="border rounded-lg p-3">
                      <p><strong>Title:</strong> {chunk.title}</p>
                      <p><strong>Source Type:</strong> {chunk.source_type}</p>
                      <p><strong>Text:</strong> {chunk.text}</p>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
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

        {scrapeHistory.length > 0 && (
          <div className="border rounded-lg p-4 mt-4 space-y-3">
            <h3 className="text-xl font-semibold">Saved Scrape History</h3>

            <ul className="space-y-3">
              {scrapeHistory.map((scrape) => (
                <li key={scrape.id} className="border rounded-lg p-3">
                  <p>
                    <strong>Title:</strong> {scrape.title}
                  </p>
                  <p>
                    <strong>URL:</strong> {scrape.url}
                  </p>
                  <p>
                    <strong>Meta Description:</strong> {scrape.meta_description}
                  </p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>
    </main>
  );
}