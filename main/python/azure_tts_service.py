"""
Azure TTS 服务类
提供文本转语音功能，支持多种中文语音
"""
import os
import logging
import azure.cognitiveservices.speech as speechsdk


class AzureTTSService:
    """Azure TTS 服务类"""
    
    def __init__(self):
        """初始化 Azure TTS 服务"""
        self.speech_key = os.getenv('SPEECH_KEY')
        self.speech_region = os.getenv('SPEECH_REGION')
        
        if not self.speech_key or not self.speech_region:
            raise ValueError("环境变量 SPEECH_KEY 和 SPEECH_REGION 必须设置")
        
        # 创建语音配置
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, 
            region=self.speech_region
        )
        
        # 设置音频输出格式
        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
        )
        
        # 支持的中文语音列表
        self.supported_voices = {
            # 女声
            'xiaoxiao': 'zh-CN-XiaoxiaoNeural',
            'xiaoyi': 'zh-CN-XiaoyiNeural',
            'yunxi': 'zh-CN-YunxiNeural',
            'yunxia': 'zh-CN-YunxiaNeural',
            'xiaochen': 'zh-CN-XiaochenNeural',
            'xiaohan': 'zh-CN-XiaohanNeural',
            'xiaomeng': 'zh-CN-XiaomengNeural',
            'xiaomo': 'zh-CN-XiaomoNeural',
            'xiaoxuan': 'zh-CN-XiaoxuanNeural',
            'xiaoyan': 'zh-CN-XiaoyanNeural',
            'yaoyao': 'zh-CN-YaoyaoNeural',
            # 男声
            'yunyang': 'zh-CN-YunyangNeural',
            'yunye': 'zh-CN-YunyeNeural',
            # 童声
            'yundeng': 'zh-CN-YundengNeural'
        }
        
        # 设置默认语音
        self.default_voice = 'xiaoxiao'
        
        # 语音描述信息
        self.voice_descriptions = {
            'xiaoxiao': '女声，自然温柔，适合日常对话',
            'xiaoyi': '女声，年轻活泼，适合轻松内容',
            'yunxi': '女声，成熟稳重，适合正式场合',
            'yunxia': '女声，亲切友善，适合教育内容',
            'xiaochen': '女声，清新自然，适合新闻播报',
            'xiaohan': '女声，温暖亲切，适合故事讲述',
            'xiaomeng': '女声，甜美可爱，适合儿童内容',
            'xiaomo': '女声，优雅知性，适合文学朗诵',
            'xiaoxuan': '女声，清澈明亮，适合广告配音',
            'xiaoyan': '女声，沉稳大气，适合纪录片',
            'yaoyao': '女声，柔和甜美，适合情感表达',
            'yunyang': '男声，沉稳有力，适合商务场合',
            'yunye': '男声，温和亲切，适合生活内容',
            'yundeng': '童声，天真活泼，适合儿童故事'
        }
        
        logging.info("Azure TTS 服务初始化完成")
    
    def get_voice_name(self, voice_key):
        """根据语音键获取语音名称"""
        return self.supported_voices.get(voice_key, self.supported_voices[self.default_voice])
    
    def synthesize_speech(self, text, voice='xiaoxiao', rate=1.0):
        """
        合成语音
        
        Args:
            text (str): 要转换的文本
            voice (str): 语音类型 (xiaoxiao, yaoyao, yunyang)
            rate (float): 语速因子
            
        Returns:
            bytes: WAV 格式的音频数据
        """
        try:
            # 设置语音
            voice_name = self.get_voice_name(voice)
            self.speech_config.speech_synthesis_voice_name = voice_name
            
            # 创建合成器
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config, 
                audio_config=None
            )
            
            # 构建 SSML，控制语速 - Azure TTS 支持直接使用小数作为语速因子
            # rate=1.0 -> 正常语速, rate=0.5 -> 0.5倍速, rate=2.0 -> 2.0倍速
            ssml = f"""
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
                <voice name="{voice_name}">
                    <prosody rate="{rate}">
                        {text}
                    </prosody>
                </voice>
            </speak>
            """

            text_length = len(text)
            azure_endpoint = (
                f"https://{self.speech_region}.tts.speech.microsoft.com/cognitiveservices/v1"
            )
            logging.info(
                "Azure TTS 请求: voice=%s, rate=%.2f, 文本长度=%d",
                voice_name,
                rate,
                text_length,
            )
            logging.debug("Azure Endpoint: %s", azure_endpoint)

            # 执行语音合成
            result = synthesizer.speak_ssml_async(ssml).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logging.info(
                    "语音合成成功: voice=%s, 文本长度=%d",
                    voice_name,
                    text_length,
                )
                return result.audio_data
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speechsdk.SpeechSynthesisCancellationDetails.from_result(result)
                logging.error(f"语音合成被取消: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    logging.error(f"错误详情: {cancellation_details.error_details}")
                raise Exception(f"语音合成失败: {cancellation_details.error_details}")
            else:
                raise Exception("语音合成失败: 未知错误")
                
        except Exception as e:
            logging.error(f"语音合成异常: {str(e)}")
            raise
    
    def check_connection(self):
        """检查 Azure TTS 连接"""
        try:
            # 尝试合成一个简单的测试文本
            test_audio = self.synthesize_speech("测试", self.default_voice, 1.0)
            return test_audio is not None and len(test_audio) > 0
        except Exception as e:
            logging.error(f"Azure TTS 连接检查失败: {str(e)}")
            return False
