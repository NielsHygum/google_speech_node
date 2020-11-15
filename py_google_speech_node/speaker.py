import rclpy
from rclpy.node import Node
from google.cloud import texttospeech
from std_msgs.msg import String
import simpleaudio as sa


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.tts_client = texttospeech.TextToSpeechClient()
        self.tts_voice = texttospeech.VoiceSelectionParams(language_code="nb-NO", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
        self.tts_audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16, sample_rate_hertz=48000)


    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        synthesis_input = texttospeech.SynthesisInput(text=msg.data)
        response = self.tts_client.synthesize_speech(input=synthesis_input, voice=self.tts_voice, audio_config=self.tts_audio_config)
        play_obj = sa.play_buffer(response.audio_content, 1, 2, 48000)
        play_obj.wait_done()




def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
