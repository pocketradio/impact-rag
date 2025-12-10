"use client";

import { useEffect, useState } from "react";

export default function QueryPage() {
	const [repoUrl, setRepoUrl] = useState("");
	const [question, setQuestion] = useState("");
	const [loading, setLoading] = useState(false);
	const [answer, setAnswer] = useState("");
    const [repo_id, setRepo_id] = useState("");

	useEffect(() => {
		const savedUrl = localStorage.getItem("repo_url");
		if (savedUrl) setRepoUrl(savedUrl);
        const saved_id = localStorage.getItem("repo_id");
        if ( saved_id) setRepo_id(saved_id);
	}, []);

    console.log(repoUrl, 'is the url');
	async function askRepo() {
		if (!question.trim()) return;

		setLoading(true);
		setAnswer("");

		try {
			const res = await fetch("http://localhost:8000/query", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					user_query: question,
					repo_id: repo_id,
					repo_url: repoUrl,
				}),
			});

			const data = await res.json();

			const content = data?.content || "No content returned.";
			setAnswer(content);

		} catch (err) {
			setAnswer("Query failed.");
		}

		setLoading(false);
	}

	return (
		<div className="space-y-6">
			
			<h1 className="text-3xl font-bold text-orange-400">
				Query The Repository
			</h1>


			<div className="text-sm">
				<p className="text-orange-500 font-semibold">Repository:</p>

				<div className="mt-1 bg-black border border-orange-600 rounded-lg px-4 py-3 text-orange-300 text-xs break-words">
					{repoUrl || "No repository selected yet"}
				</div>
			</div>

	
			<div className="bg-black border-2 border-orange-500 rounded-lg px-4 py-3">
				<input
					placeholder="Ask something about the code…"
					value={question}
					onChange={(e) => setQuestion(e.target.value)}
					className="bg-black text-orange-300 placeholder-orange-700 w-full outline-none"
				/>
			</div>

			<button
				className="bg-orange-500 hover:bg-orange-600 text-black px-5 py-2.5 rounded-lg font-semibold transition"
				disabled={loading}
				onClick={askRepo}
			>
				{loading ? "Searching..." : "Ask"}
			</button>

			{answer && (
				<div className="bg-black border border-orange-700 rounded-lg p-4 text-sm whitespace-pre-wrap">
					{answer}
				</div>
			)}

		</div>
	);
}
