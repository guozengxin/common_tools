<?php

	function load_file_content($filepath) {
		$body = "";
		$file = fopen($filepath, "r");
		if (!$file) {
			die("Cannot open $filepath");
		}
		while (!feof($file)) {
			$body .= fgets($file, 4096);
		}
		return $body;
	}

	$options = getopt("u:f:n:t:s:b:B:a:m:");

	if (array_key_exists("u", $options)) {
		$uid = $options["u"];
	} else {
		$uid = "tianwei@sogou-inc.com";
	}

	if (array_key_exists("f", $options)) {
		$from_mail = $options["f"];
	} else {
		die("set from-mail by -f\n");
	}

	if (array_key_exists("n", $options)) {
		$from_name = $options["n"];
	} else {
		$from_name = $from_mail;
	}

	if (array_key_exists("t", $options)) {
		$mailliststr = $options["t"];
		$maillist = split(";", $mailliststr);
	} else {
		die("set mail-list by -t\n");
	}

	if (array_key_exists("s", $options)) {
		$subject = $options["s"];
	} else {
		$subject = "";
	}

	$body = "";
	if (array_key_exists("b", $options)) {
		$body = $options["b"];
	} else if (array_key_exists("B", $options)) {
		$body_file = $options["B"];
		$body = load_file_content($body_file);
	} else {
		die("set body by -b or set body-file by -B\n");
	}

	$attachment_body = "";
	if (array_key_exists("a", $options)) {
		$attachment_path = $options["a"];
		$attachment_body = load_file_content($attachment_path);
	} else {
		$attachment_path = "";
	}

	if (array_key_exists("m", $options)) {
		$mode = $options["m"];
		if ($mode == "html" || $mode == "htm") {
			$mode = "html";
		} else if ($mode == "text" || $mode == "txt") {
			$mode = "txt";
		} else {
			die("set mode by -m html -m text\n");
		}
	} else {
		$mode = "txt";
	}

#		http://portal.sys.sogou-op.org/portal/tools/send_mail.php
#
#		uid - 申请权限的user_id，请使用sogou-inc邮箱账号
#		fr_name - 发信人姓名
#		fr_addr - 发信人email
#		title - 邮件标题
#		body - 邮件内容
#		mode - 邮件类型，html或txt
#		maillist - 收信人邮箱，多个邮箱用";"分隔
#		attname - 附件文件名
#		attbody - 附件正文

	$handle = curl_init();

	$post = array();
	$post["uid"] = $uid;
	$post["fr_addr"] = $from_mail;
	$post["fr_name"] = $from_name;
	$post["title"] = $subject;
	$post["body"] = $body;
	$post["mode"] = $mode;
	$post["maillist"] = $mailliststr;
	if ($attachment_path != "") {
		$post["attname"] = basename($attachment_path);
		$post["attbody"] = $attachment_body;
	}

	curl_setopt($handle, CURLOPT_POST, 1);
	curl_setopt($handle, CURLOPT_POSTFIELDS, $post);
	curl_setopt($handle, CURLOPT_URL, "http://portal.sys.sogou-op.org/portal/tools/send_mail.php");
	curl_setopt($handle, CURLOPT_RETURNTRANSFER,1);
	$content = curl_exec($handle);

	#$mailer = new mailer($from_mail, $from_name, $subject, $body);
	#$mailer->mail($maillist, $mode, $cc, $bcc, $attachment, $inlineimage);
?>
