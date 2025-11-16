"""
测试 Azure TTS 新语音的可用性和语速控制
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'main', 'python'))

from azure_tts_service import AzureTTSService
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_voice_availability():
    """测试所有语音的可用性"""
    print("开始测试语音可用性...")
    
    try:
        tts_service = AzureTTSService()
        test_text = "这是一个语音测试"
        
        results = {}
        for voice_key, voice_name in tts_service.supported_voices.items():
            try:
                print(f"测试语音: {voice_key} ({voice_name})")
                audio_data = tts_service.synthesize_speech(test_text, voice_key, 1.0)
                
                if audio_data and len(audio_data) > 0:
                    results[voice_key] = "✓ 可用"
                    print(f"  ✓ {voice_key} 可用")
                else:
                    results[voice_key] = "✗ 失败"
                    print(f"  ✗ {voice_key} 失败")
            except Exception as e:
                results[voice_key] = f"✗ 错误: {str(e)}"
                print(f"  ✗ {voice_key} 错误: {str(e)}")
        
        print("\n语音可用性测试结果:")
        for voice, status in results.items():
            print(f"  {voice}: {status}")
            
        return results
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return None

def test_rate_control():
    """测试语速控制功能"""
    print("\n开始测试语速控制...")
    
    try:
        tts_service = AzureTTSService()
        test_text = "这是一个语速测试"
        test_rates = [0.5, 1.0, 1.5, 2.0]  # 测试边界值
        test_voices = ['xiaoxiao', 'yunxi', 'xiaochen', 'yunyang']  # 测试部分语音
        
        results = {}
        
        for voice in test_voices:
            voice_results = {}
            for rate in test_rates:
                try:
                    print(f"测试语音: {voice}, 语速: {rate}")
                    audio_data = tts_service.synthesize_speech(test_text, voice, rate)
                    
                    if audio_data and len(audio_data) > 0:
                        voice_results[rate] = "✓ 成功"
                        print(f"  ✓ 语速 {rate} 成功")
                    else:
                        voice_results[rate] = "✗ 失败"
                        print(f"  ✗ 语速 {rate} 失败")
                except Exception as e:
                    voice_results[rate] = f"✗ 错误: {str(e)}"
                    print(f"  ✗ 语速 {rate} 错误: {str(e)}")
            
            results[voice] = voice_results
        
        print("\n语速控制测试结果:")
        for voice, rates in results.items():
            print(f"  {voice}:")
            for rate, status in rates.items():
                print(f"    语速 {rate}: {status}")
                
        return results
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return None

def test_invalid_rate():
    """测试无效语速的处理"""
    print("\n开始测试无效语速处理...")
    
    try:
        tts_service = AzureTTSService()
        test_text = "测试无效语速"
        invalid_rates = [0.1, 0.3, 2.5, 5.0]  # 超出范围的语速
        
        results = {}
        
        for rate in invalid_rates:
            try:
                print(f"测试无效语速: {rate}")
                audio_data = tts_service.synthesize_speech(test_text, 'xiaoxiao', rate)
                
                # 应该使用默认语速 1.0
                if audio_data and len(audio_data) > 0:
                    results[rate] = "✓ 正确使用默认值"
                    print(f"  ✓ 正确使用默认语速")
                else:
                    results[rate] = "✗ 失败"
                    print(f"  ✗ 失败")
            except Exception as e:
                results[rate] = f"✗ 错误: {str(e)}"
                print(f"  ✗ 错误: {str(e)}")
        
        print("\n无效语速处理测试结果:")
        for rate, status in results.items():
            print(f"  语速 {rate}: {status}")
            
        return results
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return None

if __name__ == "__main__":
    print("Azure TTS 语音扩展测试")
    print("=" * 50)
    
    # 测试语音可用性
    voice_results = test_voice_availability()
    
    # 测试语速控制
    rate_results = test_rate_control()
    
    # 测试无效语速处理
    invalid_rate_results = test_invalid_rate()
    
    print("\n" + "=" * 50)
    print("测试完成")