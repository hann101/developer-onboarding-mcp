from typing import List, Dict, Any
import google.generativeai as genai
from app.core.config import settings


class LLMService:
    """LLM(Gemini) 서비스"""
    
    def __init__(self):
        self.model = None
        self._initialize_models()
    
    def _initialize_models(self):
        """모델 초기화"""
        try:
            if settings.google_api_key:
                genai.configure(api_key=settings.google_api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
                print("✅ LLM 서비스가 'gemini-1.5-flash-latest' 모델로 초기화되었습니다.")
            else:
                raise ValueError("Google API 키가 설정되지 않았습니다.")
        except Exception as e:
            print(f"❌ LLM 모델 초기화 실패: {e}")
            self.model = None
    
    def generate_answer(self, question: str, context_chunks: List[str]) -> Dict[str, Any]:
        """컨텍스트를 기반으로 질문에 대한 답변 생성"""
        if not self.model:
            raise ValueError("LLM 모델이 초기화되지 않았습니다.")
            
        try:
            return self._generate_gemini_answer(question, context_chunks)
                
        except Exception as e:
            print(f"❌ 답변 생성 실패: {e}")
            raise
    
    def _generate_gemini_answer(self, question: str, context_chunks: List[str]) -> Dict[str, Any]:
        """Google Gemini를 사용한 답변 생성"""
        try:
            # 컨텍스트 조합
            context = "\n\n".join(context_chunks)
            
            # 프롬프트 구성
            prompt = f"""당신은 개발자를 위한 기술 문서 Q&A 어시스턴트입니다.

컨텍스트:
{context}

질문: {question}

위 컨텍스트를 기반으로 질문에 답변해주세요. 컨텍스트에 없는 정보는 언급하지 마시고, 명확하고 구조화된 답변을 제공해주세요."""
            
            response = self.model.generate_content(prompt)
            answer = response.text
            
            # 신뢰도 평가
            confidence = self._calculate_confidence(context_chunks, answer)
            
            return {
                "answer": answer,
                "confidence": confidence,
                "model": "Google Gemini 1.5 Flash",
                "sources_used": len(context_chunks)
            }
            
        except Exception as e:
            print(f"❌ Gemini 답변 생성 실패: {e}")
            raise
    
    def _calculate_confidence(self, context_chunks: List[str], answer: str) -> float:
        """답변의 신뢰도 계산 (간단한 휴리스틱)"""
        try:
            # 컨텍스트 길이 기반 신뢰도
            total_context_length = sum(len(chunk) for chunk in context_chunks)
            
            # 답변 길이와 컨텍스트 길이의 비율
            answer_length = len(answer)
            
            if total_context_length == 0:
                return 0.0
            
            # 기본 신뢰도 계산
            base_confidence = min(1.0, answer_length / (total_context_length * 0.1))
            
            # 컨텍스트 개수에 따른 보정
            context_bonus = min(0.2, len(context_chunks) * 0.05)
            
            final_confidence = min(1.0, base_confidence + context_bonus)
            
            return round(final_confidence, 2)
            
        except Exception:
            return 0.5  # 기본값
    
    def get_model_info(self) -> Dict[str, Any]:
        """모델 정보 조회"""
        return {
            "available_models": [
                {
                    "name": "Google Gemini 1.5 Flash",
                    "provider": "Google",
                    "status": "available"
                }
            ],
            "default_model": "Google Gemini 1.5 Flash"
        }


# 전역 LLM 서비스 인스턴스
llm_service = LLMService() 