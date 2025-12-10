"use client";

import { randomUUID } from "crypto";
import { useState } from "react";

export default function RepoPage() {
	const [repoUrl, setRepoUrl] = useState("");
	const [loading, setLoading] = useState(false);
	const [response, setResponse] = useState("");

	async function ingestRepo() {
		if (!repoUrl.trim()) return;
		setLoading(true);
		setResponse("");

        const id = crypto.randomUUID();


		try {
			const res = await fetch("http://localhost:8000/ingest", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					repo_url: repoUrl,
					// repo_id: crypto.randomUUID()
                    repo_id : id
				}),
			});

			const data = await res.json();

            localStorage.setItem("repo_url", repoUrl); // storing for access in /query instead of global state mgmt
            localStorage.setItem("repo_id", id);


			setResponse(JSON.stringify(data, null, 2));  // to format it better for readability
            if ( response ){
                console.log(response, "is the response");
            }
		} catch (e){
            console.log(e);
			setResponse("Failed to ingest repository.");
		}

		setLoading(false);
	}

	return (
		<div className="space-y-6">
			
			<h1 className="text-3xl font-bold text-orange-400">
				Connect a Repository
			</h1>

			<p className="text-orange-200/70 text-sm">
				Paste a GitHub repository URL to ingest code for analysis.
			</p>

			<div className="bg-black border-2 border-orange-500 rounded-lg px-4 py-3">
				<input
					placeholder="https://github.com/user/repository"
					value={repoUrl}
					onChange={(e) => setRepoUrl(e.target.value)}
					className="bg-black text-orange-300 placeholder-orange-700 w-full outline-none"
				/>
			</div>

			<button
				className="bg-orange-500 hover:bg-orange-600 font-semibold text-black px-5 py-2.5 rounded-lg transition"
				onClick={ingestRepo}
				disabled={loading}
			>
				{loading ? "Ingesting..." : "Ingest Repository"}
			</button>

			{response && (
				<pre className="bg-black border border-orange-700 rounded-lg p-3 text-xs whitespace-pre-wrap">
					{response}
				</pre>
			)}

		</div>
	);
}