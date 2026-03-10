import axios from "axios";

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL
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