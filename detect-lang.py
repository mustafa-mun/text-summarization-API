from lingua import LanguageDetectorBuilder

def detect_language_of_text(text):
  detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build() 
  return detector.detect_language_of(text)
