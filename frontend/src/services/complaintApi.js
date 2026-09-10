const API_BASE_URL = "http://127.0.0.1:8000";

export async function processComplaint(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/process-complaint`,
    {
      method: "POST",
      body: formData,
    },
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Complaint processing failed.",
    );
  }

  return data;
}

export async function processText(text) {
  const response = await fetch(
    `${API_BASE_URL}/api/process-text`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text,
      }),
    },
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Complaint text processing failed.",
    );
  }

  return data;
}

export async function editComplaint(message, currentForm) {
  const response = await fetch(
    `${API_BASE_URL}/api/chat`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
        current_form: currentForm,
      }),
    },
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Complaint editing failed.",
    );
  }

  return data;
}

export async function saveComplaint(complaint, riskAssessment) {
  const response = await fetch(`${API_BASE_URL}/api/save-complaint`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      complaint,
      risk_assessment: riskAssessment,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    const message =
      typeof data.detail === "string"
        ? data.detail
        : data.detail?.message || "Failed to commit complaint.";

    throw new Error(message);
  }

  return data;
}