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
		"default"		: ("เดิม","ดังเดิม","ดั้งเดิม","แบบเดิม","ต้นฉบับ","def","default")
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
		"_unknown"								:	"ไม่ทราบ",
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
		"_http_status_429_fix"					:	"คุณได้ส่งคำร้องขอมากเกินจำเป็น กรุณาเข้าไปที่ https://discordapp.com/developers/docs/topics/rate-limits#rate-limits สำหรับข้อมูลเพิ่มเติม",
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
		"_help_desc"							:	'เขียนโดย gongpha#0298',
		"_help_other"							:	"ยังไม่บอก หาเอาเอง XD",
		"_not_found_with"						:	"ไม่พบ `{0}`",
		"_incorrect_with"						:	"ข้อมูลไม่ถูกต้อง `{0}`",
		"_help_you_mean_this"					:	"หรือคุณอาจหมายถึง `{0}`",
		"_help_you_mean_this_because"			:	"หรือคุณอาจหมายถึง `{0}` ซึ่ง{1}",
		"_help_i_think_its_this"				:	"เราว่าคุณกำลังบอกว่า มันหมายถึง `{0}`",
		"_avatar_request"						:	"`{0}` : {1}",
		"_avatar_request_size"					:	"`{0}` (ขนาด : {1}) : {2}",
		"_avatar_request_nourl"					:	"`{0}` (ขนาด : {1})",
		"_default_input"						:	"เป็นข้อมูลเดิม",
		"_response_everyone"					:	"มีอะไรเกิดขึ้นวะ !?",
		"_response_user"						:	"อะไรเหรอ ? {0}",
		"_response_self"						:	"นี่เราจะพูดถึงตัวเองเพื่ออะไรเนี่ย ? XD",
		"_response_rich_invite_spotify"			:	"ไม่อยากฟังอ่ะ ฟังไม่เป็น XD",

		"_template_obsolete_command"			:	"คำสั่ง `{0}` ล้าสมัย และถูกถอนการใช้งาน",
		"_template_try_new_command"				:	"ลองคำสั่งใหม่ดูสิ ? {0}",

		"_section_head_general"					:	"ทั่วไป",
		"_section_head_generator"				:	"ตัวกำเนิด",
		"_section_head_calculator"				:	"เครื่องคิดเลข",
		"_section_head_karaoke"					:	"คาราโอเกะ",
		"_section_head_image"					:	"รูปภาพ",
		"_section_head_gen_image"				:	"สร้างรูป",
		"_section_head_summon_thai"				:	"แซวคน",

		"_need_quote_for_space"					:	"""จำเป็นใช้เครื่องหมายอัญประกาศ (") หากข้อความมีเว้นวรรค""",
		"_dont_need_quote_if_space"				:	"""ไม่ต้องใช้เครื่องหมายอัญประกาศ (") แม้ข้อความมีเว้นวรรค""",
		"_dont_need_quote_if_space_but_config"	:	"""ไม่ต้องใช้เครื่องหมายอัญประกาศ (") แม้ข้อความมีเว้นวรรค แต่ไม่สามารถปรับแต่งได้"""

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

commandinfo = {
	"th" : {
		"wanbuaban" : (
			"สร้างคาราโอเกะ วังบัวบาน",
			"<ข้อความ> <สีของข้อความ = สุ่ม> <ร้อยละของสีที่ถูกกลืนไป = สุ่มจาก 10 ถึง 100> <ภาพ = จากภาพล่าสุดหรือจากภาพโปรไฟล์ของตัวเอง>",
			(stringstack["th"]["_need_quote_for_space"]),
			(("wanbuaban",stringstack["th"]["_dont_need_quote_if_space"]))
		),
		"topline" : (
			"สร้างคาราโอเกะ ท็อปไลน์-ไดมอนด์ ปี พ.ศ. 2533",
			"<ข้อความ> <สีของข้อความ = สุ่ม> <ร้อยละของสีที่ถูกกลืนไป = สุ่มจาก 10 ถึง 100> <ภาพ = จากภาพล่าสุดหรือจากภาพโปรไฟล์ของตัวเอง>",
			(stringstack["th"]["_need_quote_for_space"]),
			(("topline",stringstack["th"]["_dont_need_quote_if_space_but_config"]))
		),
		"ncfunt" : (
			"""
			ใช้ NCFUnt ในการสร้างข้อความโดยใช้แม่แบบของตัวเอง
			ใช้ [] ในการสร้างกล่องข้อความที่จะใช้สุ่มโดยใช้ | ในการแบ่งข้อความ
			อย่างเช่น :
			   `[a|b|c]` : สุ่ม a b c มาอย่างใดอย่างหนึ่ง
			   `I am a [boy|girl|dog|cat] : ผลออกมาที่เป็นไปได้
			      `I am a boy`
				  `I am a girl`
				  `I am a dog`
				  `I am a cat`
			""",
			"<แม่แบบ>"
		),
		"mention" : (
			"กล่าวถึงผู้ใช้นั้นพร้อมจำนวนไม่เกิน 25 ครั้ง",
			"<การกล่าวถึงสมาชิก... = ตัวเอง>"
		),
		"avatar" : (
			"ส่ง URL รูปโปรไฟล์ของคน ๆ นั้น (นามสกุลไฟล์ `webp`)",
			"<การกล่าวถึงผู้ใช้ = ตัวเอง>"
		),
		"avatar_png" : (
			"ส่ง URL รูปโปรไฟล์ของคน ๆ นั้น (นามสกุลไฟล์ `png`)",
			"<การกล่าวถึงผู้ใช้ = ตัวเอง>"
		),
		"infoimg" : (
			"ส่งข้อมูลของผู้ใช้แบบรายละเอียดผ่านรูปภาพ (ไม่เสถียร)",
			"<การกล่าวถึงผู้ใช้... = ตัวเอง>"
		),
		"gaussianblur" : (
			"เบลอภาพด้วย Gaussian",
			"<ขนาด = 2, ภาพ = จากภาพล่าสุดหรือจากภาพโปรไฟล์ของตัวเอง>"
		),
		"boxblur" : (
			"เบลอภาพด้วย Box",
			"<ขนาด = 2, ภาพ = จากภาพล่าสุดหรือจากภาพโปรไฟล์ของตัวเอง>"
		),
		"ก็มาดิครับ" : (
			"ใช้ `ก็มาดิครับ !` กับผู้ใช้คนนั้น",
			"<การกล่าวถึงผู้ใช้...>"
		),
		"resize" : (
			"""
			ปรับขนาดของรูปภาพ

			สำหรับการคำนวณตัวอย่าง ให้ใช้การตั้งค่าต่อไปนี้
			   `nearest` : เพื่อนบ้านใกล้สุด (คุณภาพต่ำ, เร็ว)
	   		   `bilinear` : เชิงเส้น (คุณภาพกลาง, เร็วน้อยกว่า)
	   		   `bicubic` : เส้นโค้ง (คุณภาพสูง, ช้า)
	   		   `lanczos` : Lanczos (คุณภาพสูงกว่า, ช้ามากกว่า)
			""",
			"<กว้าง> <ยาว = กว้าง> <คำนวณ = bilinear (เชิงเส้น)> <ภาพ = จากภาพล่าสุดหรือจากภาพโปรไฟล์ของตัวเอง>"
		),
		"กูรู้หมดแล้ว" : (
			"""
			ใส่ข้อความในป้าย "กูรู้หมดแล้ว" ของกำนันโชติ
			""",
			"<ข้อความ (ไม่ควรเกิน 15 ตัวอักษร)>"
		),
		"avatar_circle" : (
			"ส่งรูปโปรไฟล์ของคน ๆ นั้นแบบกลม (นามสกุลไฟล์ `png`)",
			"<การกล่าวถึงผู้ใช้... = ตัวเอง>"
		),
	}
}
