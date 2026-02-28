import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

export const analyzeResume = async (file, jobDescription) => {
  const formData = new FormData();
  formData.append("resume", file);
  formData.append("job_description", jobDescription);

  const response = await API.post("/analyze", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });

  return response.data;
};