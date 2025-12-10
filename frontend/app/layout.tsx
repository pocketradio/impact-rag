import "./globals.css";

export const metadata = {
	title: "Code RAG",
	description: "AI Code Analysis for Repositories",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
	return (
		<html lang="en">
			<body className="bg-black text-orange-300">
				<div className="min-h-screen flex">

					<aside className="w-60 p-6 border-r-2 border-orange-600 hidden md:flex flex-col gap-6">
						<h1 className="text-2xl font-bold text-orange-500">CodeRAG</h1>

						<nav className="flex flex-col gap-2">
							<a
								href="/repo"
								className="px-3 py-2 rounded-md hover:bg-orange-800/20 border border-transparent hover:border-orange-500 transition"
							>
								Repository Setup
							</a>

							<a
								href="/query"
								className="px-3 py-2 rounded-md hover:bg-orange-800/20 border border-transparent hover:border-orange-500 transition"
							>
								Query Repo
							</a>
						</nav>
					</aside>

					<main className="flex-1 flex items-center justify-center p-8">
						<div className="w-full max-w-3xl">
							{children}
						</div>
					</main>
				</div>
			</body>
		</html>
	);
}
