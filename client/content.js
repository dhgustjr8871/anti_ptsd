const SERVER_URL = "http://localhost:5000/blip";

function isBase64Image(src) {
  return src.startsWith("data:image/");
}

function createOverlay(img, caption) {
  const rect = img.getBoundingClientRect();
  const overlay = document.createElement("div");

  overlay.textContent = caption;
  overlay.style.position = "absolute";
  overlay.style.left = `${rect.left + window.scrollX}px`;
  overlay.style.top = `${rect.top + window.scrollY}px`;
  overlay.style.width = `${rect.width}px`;
  overlay.style.height = `${rect.height}px`;
  overlay.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
  overlay.style.color = "white";
  overlay.style.fontSize = "12px";
  overlay.style.padding = "4px";
  overlay.style.zIndex = "9999";
  overlay.style.display = "flex";
  overlay.style.alignItems = "center";
  overlay.style.justifyContent = "center";
  overlay.style.pointerEvents = "none";

  document.body.appendChild(overlay);
}

async function analyzeImage(img) {
  const src = img.src;
  let body;

  if (isBase64Image(src)) {
    const base64Data = src.split(",")[1];
    body = JSON.stringify({ base64: base64Data });
  } else if (src.startsWith("http")) {
    body = JSON.stringify({ url: src });
  } else {
    console.warn("❗ 지원되지 않는 이미지:", src);
    return;
  }

  try {
    const res = await fetch(SERVER_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body
    });

    const data = await res.json();
    if (data.caption) {
      console.log("🔍 문장 추출:", data.caption);
      createOverlay(img, data.caption);
    }
  } catch (err) {
    console.error("❌ BLIP 요청 실패:", err);
  } finally {
    img.style.visibility = "visible";  // 이미지 다시 보이게
  }
}

// 이미지를 순차적으로 처리
async function processImagesSequentially(images) {
  for (const img of images) {
    await analyzeImage(img);
  }
}

function run() {
  const images = [...document.images].filter(img => img.complete && img.naturalWidth !== 0);
  
  // 일단 모두 숨기기
  images.forEach(img => {
    img.style.visibility = "hidden";
  });

  // 순차 처리 시작
  processImagesSequentially(images);
}

run();
