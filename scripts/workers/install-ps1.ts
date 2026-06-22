// Cloudflare Pages Function for install.ps1 redirect
export const onRequest: PagesFunction = async () => {
  const response = await fetch("https://api.github.com/repos/librefang/librefang/releases/latest", {
    headers: {
      "Accept": "application/vnd.github+json",
      "User-Agent": "librefang-website"
    }
  });

  const data = await response.json();
  const tag = data.tag_name;

  // Find the Windows x86_64 zip asset
  const asset = data.assets?.find((a: any) => a.name.includes("x86_64-pc-windows-msvc.zip"));

  if (asset) {
    return Response.redirect(asset.browser_download_url, 302);
  }

  return new Response("No release found", { status: 404 });
};
