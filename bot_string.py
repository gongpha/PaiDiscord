# commands[strWithMonospace(cmd_prefix+'mention')]='Mention to user'
# commands[strWithMonospace(cmd_prefix+'mentionme')]='Mention self'
# commands[strWithMonospace(cmd_prefix+'avatar')]="Give user's avatar URL"
# commands[strWithMonospace(cmd_prefix+'myavatar')]='Give my avatar URL'
# commands[strWithMonospace(cmd_prefix+'ncfunt')]='Call NCFU by using own template'
# commands[strWithMonospace(cmd_prefix+'mean')]='Finding Arithmetic mean'
# commands[strWithMonospace(cmd_prefix+'h_mean')]='Finding Harmonic mean'
# commands[strWithMonospace(cmd_prefix+'median')]='Finding Median (Middle)'
# commands[strWithMonospace(cmd_prefix+'infoimg')]="Send User's info"
# commands[strWithMonospace(cmd_prefix+'blur')]="Blur Image"
# commands[strWithMonospace(cmd_prefix+'gaussianblur')]="Gaussian Blur Image"
# commands[strWithMonospace(cmd_prefix+'boxblur')]="Box Blur Image"

# ภาษาไทย (Thai, Thailand)
keyword = {
	"th" : {
		"default"		: ["เดิม","ดังเดิม","ดั้งเดิม","แบบเดิม","ต้นฉบับ","def","default"]
	}
}
commandusage = {
	"th" : {
		"ncfunt"			: "<แม่แบบ>",
		"mention"			: "<การกล่าวถึงสมาชิก... = ตัวเอง>",
		"avatar_png"		: "<การกล่าวถึงสมาชิก = ตัวเอง> <ขนาด = 1024>",
		"avatar"			: "<การกล่าวถึงสมาชิก = ตัวเอง>",
		"mean"				: "<ข้อมูล...>",
		"h_mean"			: "<ข้อมูล...>",
		"median"			: "<ข้อมูล...>",
		"infoimg"			: "<การกล่าวถึงผู้ใช้... = ตัวเอง>",
		"gaussianblur"		: "<ขนาด = 2, ภาพ = จากภาพล่าสุดหรือจากภาพโปรไฟล์ของตัวเอง>",
		"boxblur"			: "<ขนาด = 2, ภาพ = จากภาพล่าสุดหรือจากภาพโปรไฟล์ของตัวเอง>",
		"gaussianblur"		: "<ภาพ = จากภาพล่าสุดหรือจากภาพโปรไฟล์ของตัวเอง>",
		"ก็มาดิครับ"			: "<การกล่าวถึงผู้ใช้...>",
		"resize"			: "<กว้าง> <ยาว = กว้าง> <คำนวณ = เชิงเส้น> <ภาพ = จากภาพล่าสุดหรือจากภาพโปรไฟล์ของตัวเอง>",
		"toplinekaraoke"	: "<ข้อความ> <สีของข้อความ = สุ่ม> <ร้อยละของสีที่ถูกกลืนไป = สุ่มจาก 10 ถึง 100> <ภาพ = จากภาพล่าสุดหรือจากภาพโปรไฟล์ของตัวเอง>"
	}
}
stringstack = {
	"th" : {
		"_bot_name"								:	"ประมวล (OpenProcess)",
		"_request_by"							:	"ถูกร้องขอโดย {0}",
		"_argument_index"						:	"ข้อมูลช่องที่ {}",
		"_error_title"							:	"❌ มีข้อผิดพลาด",
		"_error_unknown"						:	"กูไม่รู้เหมือนกันว่าข้อผิดพลาดอะไร",
		"_error_unknown_fix"					:	"ไว้อาลัยให้กับคนพิมพ์ 3 วิ",
		"_error_bad_argument"					:	"ข้อมูลเชี้ยไรเนี่ย ?",
		"_error_bad_argument_fix"				:	"เปลี่ยนข้อมูล แล้วลองใหม่ดิ",
		"_error_http"							:	"เกิดข้อผิดพลาดจาก HTTP : {0} ({1})",
		"_error_http_fix"						:	"{0}",
		"_http_status_200"						:	"ปกติ",
		"_http_status_200_fix"					:	"คำร้องขอสำเร็จ",
		"_http_status_201"						:	"ถูกสร้างแล้ว",
		"_http_status_201_fix"					:	"วัตถุถูกสร้างสำเร็จ",
		"_http_status_204"						:	"ปกติ แต่ไม่มีเนื้อหา",
		"_http_status_204_fix"					:	"คำร้องขอสำเร็จ แต่ไม่มีเนื้อหาใด ๆ ถูกส่งกลับมา",
		"_http_status_304"						:	"วัตถุไม่ได้เปลี่ยนแปลง",
		"_http_status_304_fix"					:	"วัตถุไม่ได้รับการกระทำใด ๆ",
		"_http_status_400"						:	"คำร้องขอล้มเหลว",
		"_http_status_400_fix"					:	"เซิรืฟเวอร์ไม่สามารถวิเคราะห์คำร้องขอได้",
		"_http_status_401"						:	"ไม่ได้รับอนุญาต",
		"_http_status_401_fix"					:	"การอนุญาตถูกปฏิเสธจากเซิร์ฟเวอร์ อาจจะเป็นเพราะส่วนหัวข้อของ Authorization นั้นสูญหายไป หรือ ไม่ถูกต้อง",
		"_http_status_403"						:	"ไม่มีสิทธิ์เข้าถึง",
		"_http_status_403_fix"					:	"การเข้าถึงถูกปฏิเสธจากเซิร์ฟเวอร์",
		"_http_status_404"						:	"ไม่พบเนื้อหาดังกล่าว",
		"_http_status_404_fix"					:	"ไม่พบเนื้อหาจากเวิร์ฟเวอร์จากคำร้องขอ",
		"_http_status_405"						:	"การเข้าถึงของคำร้องขอไม่ได้รับการอนุญาต",
		"_http_status_405_fix"					:	"วิธีการของ HTTP ไม่ถูกต้องสำหรับตำแหน่งที่จะเข้าถึง",
		"_http_status_429"						:	"มีคำร้องขอมากมายถูกส่งมาในเวลาเดียวกัน",
		"_http_status_429_fix"					:	"คุณได้ส่งคำร้องขอมากเกินจำเป็น กรุณาเข้าที่ https://discordapp.com/developers/docs/topics/rate-limits#rate-limits สำหรับข้อมูลเพิ่มเติม",
		"_http_status_502"						:	"เกตเวย์ไม่พร้อมใช้งาน",
		"_http_status_502_fix"					:	"เกตเวย์ไม่พร้อมใช้งานสำหรับการส่งคำร้องขอ กรุณาลองใหม่อีกครั้ง",
		"_http_status_5XX"						:	"เซิร์ฟเวอร์ผิดพลาด",
		"_http_status_5XX_fix"					:	"เซิร์ฟเวอร์มีข้อผิดพลาดในการประมวลผลคำร้องขอของคุณ",
		"_request_timeout"						:	"หมดเวลาการเชื่อมต่อ",
		"_request_timeout_fix"					:	"กรุณาลองใหม่อีกครั้ง",
		"_request_too_many_redirect"			:	"มีการเปลี่ยนเส้นทางมากเกินไป",
		"_request_too_many_redirect_fix"		:	"กรุณาลองใหม่อีกครั้ง",
		"_request_missing_schema"				:	"ขาดรูปแบบของ URL",
		"_request_missing_schema_fix"			:	'กรณาเติม "https://" หรือ "http://" หน้า URL',
		"_error_missing_required_argument"		:	"เหมือนมึงลืมบางอย่างไปนะ",
		"_error_missing_required_argument_fix"	:	"ลองคิดดูให้ดิว่าลืมอะไรไป จากนั้นใส่มันเข้าไป แล้วก็ลองใหม่",
		"_error_disabled_command"				:	"คำสั่งถูกมัดแหนมเรียบร้อย",
		"_error_disabled_command_fix"			:	"คำสั่งถูกปิดการใช้งาน เจ้าช่างกล้านะ ที่พิมพ์มันไปได้",
		"_error_command_invoke_error"			:	"คำร้องขอคำสั่งผิดพลาด",
		"_error_command_invoke_error_fix"		:	"{0}",
		"_error_int_is_not_number"				:	"{0} มันไม่ใช่ตัวเลขน่ะสิ !",
		"_error_int_is_not_number_fix"			:	"เขียน{0} ใหม่ ให้มันบ่งบอกได้ว่า มันคือตัวเลข",
		"_error_no_private_message"				:	"คำสั่งไม่สามารถเรียกใช้ในข้อความส่วนตัวได้ !",
		"_error_no_private_message_fix"			:	"เอาไปใช้ในเซิร์ฟเวอร์ ไป๊ !",
		"_error_not_found"						:	"ไม่พบข้อมูลดังกล่าว",
		"_error_not_found_fix"					:	"ลองตรวจสอบข้อมูลใหม่อีกครั้ง",
		"_error_not_found_user"					:	"ไม่พบผู้ใช้ดังกล่าว",
		"_error_not_found_user_fix"				:	"เอาง่าย ๆ คือ มันไม่มีตัวตนอยู่จริง ลองตรวจสอบข้อมูลใหม่อีกครั้ง",
		"_help_title"							:	"อาจจะช่วยไม่เยอะสักเท่าไหร่",
		"_help_more???"							:	"มีอีกไหมวะ ?",
		"_help_desc"							:	'เขียนโดย gongpha#0394\nโดยใช้ discord.py {} กับ Python {}\n*"บอทแม่งทำไรไม่ได้เลยสัส"*',
		"_help_other"							:	"ยังไม่บอก หาเอาเอง XD",
		"_help_mention_to_user"					:	"กล่าวถึงผู้ใช้ หรือ Ping ผู้ใช้ ตามจำนวน",
		"_help_avatar_user_webp"				:	"ส่ง URL รูปโปรไฟล์ของคน ๆ นั้น (webp)",
		"_help_avatar_self_webp"				:	"ส่ง URL รูปโปรไฟล์ของตัวเอง (webp)",
		"_help_ncfu"							:	"ใช้ตัวสุ่มอเนกประสงค์โดยใช้แม่แบบของตัวเอง",
		"_help_info_img_less"					:	"ส่งข้อมูลของผู้ใช้แบบรายละเอียดโคตรน้อยผ่านรูปภาพ",
		"_help_blur_image"						:	"เบลอภาพ (ทั่วไป)",
		"_help_blur_image_gaussian"				:	"เบลอภาพด้วย Gaussian (ไม่คม ไม่ชัด ไม่ลึก ดูไม่ออกแน่นอน)",
		"_help_blur_image_box"					:	"เบลอภาพด้วย Box (เหมือนคนสายตาสั้น)",
		"_not_found_with"						:	"ไม่พบ `{0}`",
		"_incorrect_with"						:	"ข้อมูลไม่ถูกต้อง `{0}`",
		"_help_you_mean_this"					:	"หรือคุณอาจหมายถึง `{0}`",
		"_help_you_mean_this_because"			:	"หรือคุณอาจหมายถึง `{0}` ซึ่ง{1}",
		"_help_i_think_its_this"				:	"เราว่าคุณกำลังบอกว่า มันหมายถึง `{0}`",
		"_avatar_request"						:	"`{0}` : {2}",
		"_avatar_request_size"					:	"`{0}` (ขนาด : {1}) : {2}",
		"_default_input"						:	"เป็นข้อมูลเดิม",
		"_response_everyone"					:	"มีอะไรเกิดขึ้นวะ !?",
		"_response_user"						:	"อะไรเหรอ ? {0}",
		"_response_self"						:	"นี่เราจะพูดถึงตัวเองเพื่ออะไรเนี่ย ? XD",
		"_response_rich_invite_spotify"			:	"ไม่อยากฟังอ่ะ ฟังไม่เป็น XD",

		"_template_obsolete_command"			:	"คำสั่ง `{0}` ล้าสมัย และถูกถอนการใช้งาน",
		"_template_try_new_command"				:	"ลองคำสั่งใหม่ดูสิ ? {0}"

	}
}