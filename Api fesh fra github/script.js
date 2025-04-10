async function fetchGitHubRepos() {
    const username = "Crisstuff"; // Your GitHub username
    const url = `https://api.github.com/users/${username}/repos`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`GitHub API returned ${response.status}`);
        }

        const repos = await response.json();
        generateRepoLinks(repos);
    } catch (error) {
        console.error("Error fetching repositories:", error);
    }
}

function generateRepoLinks(repos) {
    const repoContainer = document.getElementById("repo-list");
    repoContainer.innerHTML = ""; // Clear previous content

    repos.forEach(repo => {
        const repoElement = document.createElement("div");
        repoElement.classList.add("repo-item");
        repoElement.innerHTML = `
            <h3><a href="#" onclick="loadRepoPage('${repo.name}')">${repo.name}</a></h3>
            <p>${repo.description || "No description available."}</p>
        `;
        repoContainer.appendChild(repoElement);
    });
}

async function loadRepoPage(repoName) {
    const username = "Crisstuff";
    const readmeUrl = `https://raw.githubusercontent.com/${username}/${repoName}/main/README.md`;
    const repoUrl = `https://github.com/${username}/${repoName}`; // Get the repo URL

    try {
        const readmeResponse = await fetch(readmeUrl);
        const readmeText = readmeResponse.ok ? await readmeResponse.text() : "README not available.";
        

        // Convert Markdown to HTML using marked.js
        const formattedReadme = marked.parse(readmeText);

        document.getElementById("repo-container").innerHTML = `
            <button class="exit-button" onclick="reloadPage()">Exit</button>
            <h1>${repoName}</h1>
            <div class="m-Oversikt">
                <div class="readme-content">${formattedReadme}</div>
            </div>
            <div class="m-Bunn">
                <div class="m-Samarbeidspartnere"><b>Samarbeidspartnere</b><p>Ingen</p></div>
                <div class="m-logg"><b>Logg</b></div>
                <div class="m-resultat">
                    <b>Resultat</b>
                    <p><a href="${repoUrl}" target="_blank">${repoUrl}</a>
                    <div class="readme-content"></div>
                </div>
            </div>
        `;
    } catch (error) {
        console.error(`Error fetching README for ${repoName}:`, error);
    }
}
// Handle "Back" button
window.addEventListener("popstate", function (event) {
    if (event.state && event.state.repo) {
        loadRepoPage(event.state.repo);
    } else {
        reloadRepos();
    }
});

// Brukes for Exit button på sidene for og få med alt
function reloadPage() {
    location.reload()
}

// Load repositories on page load
fetchGitHubRepos();
