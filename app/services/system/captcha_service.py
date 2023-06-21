import base64

from captcha.image import ImageCaptcha
import random
import string

from app.utils import get_logger

logger = get_logger()


def generate_verification_validate_code(length=6):
    logger.info("generate_verification_validate_code开始获取验证码..................")
    logger.info("generate_verification_validate_code开始获取验证码..................string.ascii_uppercase={}, string.digits={}".format(string.ascii_uppercase, string.digits))

    # 生成指定长度的验证码
    validate_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
    logger.info("generate_verification_validate_code开始获取验证码validate_code={}..................".format(validate_code))
    return validate_code


def generate_verification_image(validate_code):
    logger.info("generate_verification_image, validate_code={}..................".format(validate_code))
    # 创建 ImageCaptcha 实例
    captcha = ImageCaptcha()
    logger.info("generate_verification_image 创建 ImageCaptcha 实例成功..................")
    # 生成验证码图片
    image = captcha.generate(validate_code)
    logger.info("generate_verification_image 生成验证码图片成功..................")
    encoded_image = base64.b64encode(image.tobytes()).decode('utf-8')
    logger.info("generate_verification_image 生成验证码图片成功..encoded_image={}................".format(encoded_image))
    return encoded_image
