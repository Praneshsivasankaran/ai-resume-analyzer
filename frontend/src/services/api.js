import axios from "axios";

const API = axios.create({
  baseURL: "https://Badkarma11-ai-resume-analyzer.hf.space"
});

export const analyzeResume = async (file, jobDescription) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("jd_text", jobDescription);

  const response = await API.post("/analyze", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });

  return response.data;
};