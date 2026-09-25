(() => {
  const endpoint = document.querySelector('meta[name="jev-analytics-endpoint"]')?.content.trim();
  window.jevTrack = () => {};
  if (!endpoint) return;

  let target;
  try { target = new URL(endpoint); } catch { return; }
  if (target.protocol !== "https:" || !/^[a-z0-9-]+\.goatcounter\.com$/.test(target.hostname) || target.pathname !== "/count" || target.search || target.hash) return;
  const notice = document.querySelector("#analytics-state");
  if (notice) notice.textContent = "Aggregate analytics are enabled for this visit. Details about the events and data fields appear below.";
  const setup = document.querySelector("#analytics-setup");
  if (setup) setup.textContent = "The analytics endpoint is enabled. The optional counter loads only for the configured GoatCounter site and records the limited events described above.";

  const incoming = new URLSearchParams(location.search);
  const campaign = incoming.get("utm_content") || "";
  const safeSource = incoming.get("utm_source") || "";
  const safeCampaign = incoming.get("utm_campaign") || "";
  const safeValue = value => /^[a-z0-9_-]{1,48}$/.test(value) ? value : "";
  const attribution = new URLSearchParams();
  if (safeValue(safeSource)) attribution.set("utm_source", safeSource);
  if (safeValue(safeCampaign)) attribution.set("utm_campaign", safeCampaign);
  const attributionQuery = attribution.toString();
  const cleanUrl = `${location.pathname}${attributionQuery ? `?${attributionQuery}` : ""}${location.hash}`;
  if (cleanUrl !== `${location.pathname}${location.search}${location.hash}`) history.replaceState(history.state, "", cleanUrl);
  const suffix = /^exp\d+_v\d+$/.test(campaign) ? `_${campaign}` : "";
  const queued = [];
  let ready = false;
  window.goatcounter = {
    path: location.pathname || "/",
    referrer: (() => {
      try { return document.referrer ? new URL(document.referrer).hostname : ""; }
      catch { return ""; }
    })(),
  };
  window.jevTrack = (name) => {
    if (!/^[a-z0-9_-]+$/.test(name)) return;
    const path = `${name}${suffix}`;
    if (ready && window.goatcounter?.count) {
      window.goatcounter.count({ path, title: path, event: true, no_session: true });
    } else if (queued.length < 20) queued.push(path);
  };
  document.querySelectorAll("[data-jev-event]").forEach((element) => {
    element.addEventListener("click", () => window.jevTrack(element.dataset.jevEvent));
  });

  const script = document.createElement("script");
  script.src = "https://gc.zgo.at/count.v5.js";
  script.async = true;
  script.crossOrigin = "anonymous";
  script.integrity = "sha384-atnOLvQb9t+jTSipvd75X2yginT4PjVbqDdlJAmxMm+wYElFmeR6EmLP5bYeoRVQ";
  script.dataset.goatcounter = endpoint;
  script.addEventListener("load", () => {
    ready = true;
    while (queued.length) window.jevTrack(queued.shift().replace(suffix, ""));
  });
  document.head.append(script);
})();
