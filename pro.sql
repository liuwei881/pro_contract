CREATE TABLE `capital`  (
  `id` int(11) NOT NULL PRIMARY KEY COMMENT '资金下达表主键',
  `project_id` int(11) NULL COMMENT '项目id',
  `capital_channel_id` int(11) NULL COMMENT '资金渠道id',
  `allow_file` varchar(128) NULL COMMENT '批复文件',
  `allow_money` varchar(128) NULL COMMENT '下达金额',
  PRIMARY KEY (`id`)
);

CREATE TABLE `capital_channel`  (
  `id` int(11) NOT NULL PRIMARY KEY COMMENT '资金渠道表主键',
  `name` varchar(128) NULL COMMENT '渠道名称',
  PRIMARY KEY (`id`)
);

CREATE TABLE `contract`  (
  `id` int(11) NOT NULL PRIMARY KEY COMMENT '合同id',
  `capital_channel_id` int(11) NULL COMMENT '渠道id',
  `contract_values` varchar(128) NULL COMMENT '合同值',
  `payment` varchar(128) NULL COMMENT '已支付',
  `allow_nopay` varchar(128) NULL COMMENT '已申请未支付',
  `pay_time` datetime NULL COMMENT '支付时间',
  `check_clear` varchar(128) NULL COMMENT '结算值',
  `party_unit` varchar(128) NULL COMMENT '乙方单位',
  PRIMARY KEY (`id`)
);

CREATE TABLE `project`  (
  `id` int(11) NOT NULL PRIMARY KEY COMMENT '主键',
  `capital_id` int(11) NULL COMMENT '资金下达表id',
  `contract_id` int(11) NULL COMMENT '合同id',
  `pro_name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '项目名称',
  `c_project` varchar(128) NULL COMMENT '立项',
  `research` varchar(128) NULL COMMENT '可研',
  `start` varchar(128) NULL COMMENT '初设',
  `create_time` datetime NULL COMMENT '创建时间',
  `modify_time` datetime NULL COMMENT '修改时间',
  PRIMARY KEY (`id`)
);

