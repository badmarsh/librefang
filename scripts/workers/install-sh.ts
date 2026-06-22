// Cloudflare Pages Function for install.sh redirect
export const onRequest: PagesFunction = async () => {
  const response = await fetch("https://api.github.com/repos/librefang/librefang/releases/latest", {
    headers: {
      "Accept": "application/vnd.github+json",
      "User-Agent": "librefang-website"
    }
  });

  const data = await response.json();
  const tag = data.tag_name;

  // Find the Linux x86_64 tar.gz asset
  const asset = data.assets?.find((a: any) => a.name.includes("x86_64-unknown-linux-gnu.tar.gz"));

  if (asset) {
    return Response.redirect(asset.browser_download_url, 302);
  }

  return new Response("No release found", { status: 404 });
};
