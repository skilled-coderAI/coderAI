import axios from 'axios';

const CODER_AI_BASE_URL = 'http://localhost:5000';

class CoderAIService {
  constructor() {
    this.client = axios.create({
      baseURL: CODER_AI_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async analyzeCode(code) {
    try {
      const response = await this.client.post('/analyze', { code });
      return response.data;
    } catch (error) {
      console.error('Error analyzing code:', error);
      throw error;
    }
  }

  async getProjectSuggestions() {
    try {
      const response = await this.client.get('/suggestions');
      return response.data;
    } catch (error) {
      console.error('Error getting project suggestions:', error);
      throw error;
    }
  }

  async reviewCode(codeSnippet) {
    try {
      const response = await this.client.post('/review', { code: codeSnippet });
      return response.data;
    } catch (error) {
      console.error('Error reviewing code:', error);
      throw error;
    }
  }

  async getGitHubIntegration() {
    try {
      const response = await this.client.get('/github/status');
      return response.data;
    } catch (error) {
      console.error('Error getting GitHub integration status:', error);
      throw error;
    }
  }
}

export default new CoderAIService();