#global gitcommit 10e465b5321bd53c1fc59ffab27e724535c6bc0f
%{?gitcommit:%global gitcommitshort %(c=%{gitcommit}; echo ${c:0:7})}

# We ship a .pc file but don't want to have a dep on pkg-config. We
# strip the automatically generated dep here and instead co-own the
# directory.
%global __requires_exclude pkg-config

%global pkgdir %{_prefix}/lib/systemd
%global system_unit_dir %{pkgdir}/system
%global user_unit_dir %{pkgdir}/user

Name:                 systemd
Url:                  http://www.freedesktop.org/wiki/Software/systemd
Version:              239
Release:              74%{?dist}.2
# For a breakdown of the licensing, see README
License:              LGPLv2+ and MIT and GPLv2+
Summary:              System and Service Manager

# download tarballs with "spectool -g systemd.spec"
%if %{defined gitcommit}
Source0:              https://github.com/systemd/systemd-stable/archive/%{?gitcommit}.tar.gz#/%{name}-%{gitcommitshort}.tar.gz
%else
Source0:              https://github.com/systemd/systemd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif
# This file must be available before %%prep.
# It is generated during systemd build and can be found in src/core/.
Source1:              triggers.systemd
Source2:              split-files.py
Source3:              purge-nobody-user

# Prevent accidental removal of the systemd package
Source4:              yum-protect-systemd.conf

Source5:              inittab
Source6:              sysctl.conf.README
Source7:              systemd-journal-remote.xml
Source8:              systemd-journal-gatewayd.xml
Source9:              20-yama-ptrace.conf
Source10:             systemd-udev-trigger-no-reload.conf
Source11:             20-grubby.install
Source12:             systemd-user
Source13:             rc.local

%if 0
GIT_DIR=../../src/systemd/.git git format-patch-ab --no-signature -M -N v235..v235-stable
i=1; for j in 00*patch; do printf "Patch%04d:      %s\n" $i $j; i=$((i+1));done|xclip
GIT_DIR=../../src/systemd/.git git diffab -M v233..master@{2017-06-15} -- hwdb/[67]* hwdb/parse_hwdb.py > hwdb.patch
%endif

# RHEL-specific
Patch0001:            0001-build-sys-Detect-whether-struct-statx-is-defined-in-.patch
Patch0002:            0002-logind-set-RemoveIPC-to-false-by-default.patch
Patch0003:            0003-pid1-bump-DefaultTasksMax-to-80-of-the-kernel-pid.ma.patch
Patch0004:            0004-Avoid-tmp-being-mounted-as-tmpfs-without-the-user-s-.patch
Patch0005:            0005-pid1-bump-maximum-number-of-process-in-user-slice-to.patch
Patch0006:            0006-rules-automatically-online-hot-plugged-CPUs.patch
Patch0007:            0007-rules-add-rule-for-naming-Dell-iDRAC-USB-Virtual-NIC.patch
Patch0008:            0008-rules-enable-memory-hotplug.patch
Patch0009:            0009-rules-reload-sysctl-settings-when-the-bridge-module-.patch
Patch0010:            0010-rules-load-sg-module.patch
Patch0011:            0011-rules-prandom-character-device-node-permissions.patch
Patch0012:            0012-rules-load-sg-driver-also-when-scsi_target-appears-4.patch
Patch0013:            0013-rules-don-t-hoplug-memory-on-s390x.patch
Patch0014:            0014-rules-disable-auto-online-of-hot-plugged-memory-on-I.patch
Patch0015:            0015-rules-introduce-old-style-by-path-symlinks-for-FCP-b.patch
Patch0016:            0016-Revert-udev-remove-WAIT_FOR-key.patch
Patch0017:            0017-net_setup_link-allow-renaming-interfaces-that-were-r.patch
Patch0018:            0018-units-drop-DynamicUser-yes-from-systemd-resolved.ser.patch
Patch0019:            0019-journal-remove-journal-audit-socket.patch
Patch0020:            0020-bus-move-BUS_DONT_DESTROY-calls-after-asserts.patch
Patch0021:            0021-random-seed-raise-POOL_SIZE_MIN-constant-to-1024.patch
Patch0022:            0022-cryptsetup-add-support-for-sector-size-option-9936.patch
Patch0023:            0023-cryptsetup-do-not-define-arg_sector_size-if-libgcryp.patch
Patch0024:            0024-units-don-t-enable-per-service-IP-firewall-by-defaul.patch
Patch0025:            0025-bus-message-do-not-crash-on-message-with-a-string-of.patch
Patch0026:            0026-Introduce-free_and_strndup-and-use-it-in-bus-message.patch
Patch0027:            0027-tests-backport-test_setup_logging.patch
Patch0029:            0029-resolved-create-etc-resolv.conf-symlink-at-runtime.patch
Patch0030:            0030-dissect-image-use-right-comparison-function.patch
Patch0031:            0031-login-avoid-leak-of-name-returned-by-uid_to_name.patch
Patch0032:            0032-firewall-util-add-an-assert-that-we-re-not-overwriti.patch
Patch0033:            0033-journal-file-avoid-calling-ftruncate-with-invalid-fd.patch
Patch0034:            0034-dhcp6-make-sure-we-have-enough-space-for-the-DHCP6-o.patch
Patch0035:            0035-core-rename-queued_message-pending_reload_message.patch
Patch0036:            0036-core-when-we-can-t-send-the-pending-reload-message-s.patch
Patch0037:            0037-core-make-sure-we-don-t-throttle-change-signal-gener.patch
Patch0038:            0038-proc-cmdline-introduce-PROC_CMDLINE_RD_STRICT.patch
Patch0039:            0039-debug-generator-introduce-rd.-version-of-all-options.patch
Patch0040:            0040-chown-recursive-let-s-rework-the-recursive-logic-to-.patch
Patch0041:            0041-chown-recursive-also-drop-ACLs-when-recursively-chow.patch
Patch0042:            0042-chown-recursive-TAKE_FD-is-your-friend.patch
Patch0043:            0043-test-add-test-case-for-recursive-chown-ing.patch
Patch0044:            0044-Revert-sysctl.d-request-ECN-on-both-in-and-outgoing-.patch
Patch0045:            0045-detect-virt-do-not-try-to-read-all-of-proc-cpuinfo.patch
Patch0046:            0046-sd-bus-unify-three-code-paths-which-free-struct-bus_.patch
Patch0047:            0047-sd-bus-properly-initialize-containers.patch
Patch0048:            0048-cryptsetup-generator-introduce-basic-keydev-support.patch
Patch0049:            0049-cryptsetup-don-t-use-m-if-there-s-no-error-to-show.patch
Patch0050:            0050-cryptsetup-generator-don-t-return-error-if-target-di.patch
Patch0051:            0051-cryptsetup-generator-allow-whitespace-characters-in-.patch
Patch0052:            0052-rules-watch-metadata-changes-on-DASD-devices.patch
Patch0053:            0053-sysctl.d-switch-net.ipv4.conf.all.rp_filter-from-1-t.patch
Patch0054:            0054-tests-explicitly-enable-user-namespaces-for-TEST-13-.patch
Patch0055:            0055-nspawn-beef-up-netns-checking-a-bit-for-compat-with-.patch
Patch0056:            0056-test-Drop-SKIP_INITRD-for-QEMU-based-tests.patch
Patch0057:            0057-meson-rename-Ddebug-to-Ddebug-extra.patch
Patch0058:            0058-meson-check-whether-gnutls-supports-TCP-fast-open.patch
Patch0059:            0059-unit-don-t-add-Requires-for-tmp.mount.patch
Patch0060:            0060-tests-drop-the-precondition-check-for-inherited-flag.patch
Patch0061:            0061-core-when-deserializing-state-always-use-read_line-L.patch
Patch0062:            0062-core-enforce-a-limit-on-STATUS-texts-recvd-from-serv.patch
Patch0063:            0063-travis-enable-Travis-CI-on-CentOS-7.patch
Patch0064:            0064-travis-RHEL8-support.patch
Patch0065:            0065-travis-drop-the-SELinux-Fedora-workaround.patch
Patch0066:            0066-travis-fix-syntax-error-in-.travis.yml.patch
Patch0067:            0067-travis-reboot-the-container-before-running-tests.patch
Patch0068:            0068-coredump-remove-duplicate-MESSAGE-prefix-from-messag.patch
Patch0069:            0069-journald-remove-unnecessary.patch
Patch0070:            0070-journald-do-not-store-the-iovec-entry-for-process-co.patch
Patch0071:            0071-basic-process-util-limit-command-line-lengths-to-_SC.patch
Patch0072:            0072-coredump-fix-message-when-we-fail-to-save-a-journald.patch
Patch0073:            0073-procfs-util-expose-functionality-to-query-total-memo.patch
Patch0074:            0074-basic-prioq-add-prioq_peek_item.patch
Patch0075:            0075-journal-limit-the-number-of-entries-in-the-cache-bas.patch
Patch0076:            0076-journald-periodically-drop-cache-for-all-dead-PIDs.patch
Patch0077:            0077-process-util-don-t-use-overly-large-buffer-to-store-.patch
Patch0078:            0078-Revert-sysctl.d-switch-net.ipv4.conf.all.rp_filter-f.patch
Patch0079:            0079-journal-fix-syslog_parse_identifier.patch
Patch0080:            0080-journald-set-a-limit-on-the-number-of-fields-1k.patch
Patch0081:            0081-journald-when-processing-a-native-message-bail-more-.patch
Patch0082:            0082-journald-lower-the-maximum-entry-size-limit-to-for-n.patch
Patch0083:            0083-httpd-use-a-cleanup-function-to-call-MHD_destroy_res.patch
Patch0084:            0084-journal-remote-verify-entry-length-from-header.patch
Patch0085:            0085-journal-remote-set-a-limit-on-the-number-of-fields-i.patch
Patch0086:            0086-journald-correctly-attribute-log-messages-also-with-.patch
Patch0087:            0087-test-replace-echo-with-socat.patch
Patch0088:            0088-test-network-ignore-tunnel-devices-automatically-add.patch
Patch0089:            0089-rules-add-elevator-kernel-command-line-parameter.patch
Patch0090:            0090-rule-syntax-check-allow-PROGRAM-as-an-assignment.patch
Patch0091:            0091-rules-implement-new-memory-hotplug-policy.patch
Patch0092:            0092-LGTM-make-LGTM.com-use-meson-from-pip.patch
Patch0093:            0093-lgtm-use-python3.patch
Patch0094:            0094-tools-use-print-function-in-Python-3-code.patch
Patch0095:            0095-lgtm-add-a-custom-query-for-catching-the-use-of-fget.patch
Patch0096:            0096-lgtm-drop-redundant-newlines.patch
Patch0097:            0097-rules-add-the-rule-that-adds-elevator-kernel-command.patch
Patch0098:            0098-test-add-TEST-24-UNIT-TESTS-running-all-basic-tests-.patch
Patch0099:            0099-tests-create-the-asan-wrapper-automatically-if-syste.patch
Patch0100:            0100-tests-add-a-wrapper-for-when-systemd-is-built-with-A.patch
Patch0101:            0101-tests-redirect-ASAN-reports-on-journald-to-a-file.patch
Patch0102:            0102-tests-use-the-asan-wrapper-to-boot-a-VM-container-if.patch
Patch0103:            0103-tests-allow-passing-additional-arguments-to-nspawn-v.patch
Patch0104:            0104-tests-also-run-TEST-01-BASIC-in-an-unprivileged-cont.patch
Patch0105:            0105-test-don-t-overwrite-TESTDIR-if-already-set.patch
Patch0106:            0106-bus-socket-Fix-line_begins-to-accept-word-matching-f.patch
Patch0107:            0107-Refuse-dbus-message-paths-longer-than-BUS_PATH_SIZE_.patch
Patch0108:            0108-Allocate-temporary-strings-to-hold-dbus-paths-on-the.patch
Patch0109:            0109-sd-bus-if-we-receive-an-invalid-dbus-message-ignore-.patch
Patch0110:            0110-meson-drop-misplaced-Wl-undefined-argument.patch
Patch0111:            0111-Revert-core-one-step-back-again-for-nspawn-we-actual.patch
Patch0112:            0112-tree-wide-shorten-error-logging-a-bit.patch
Patch0113:            0113-nspawn-simplify-machine-terminate-bus-call.patch
Patch0114:            0114-nspawn-merge-two-variable-declaration-lines.patch
Patch0115:            0115-nspawn-rework-how-we-allocate-kill-scopes.patch
Patch0116:            0116-unit-enqueue-cgroup-empty-check-event-if-the-last-re.patch
Patch0117:            0117-Revert-journal-remove-journal-audit-socket.patch
Patch0118:            0118-journal-don-t-enable-systemd-journald-audit.socket-b.patch
Patch0119:            0119-logs-show-use-grey-color-for-de-emphasizing-journal-.patch
Patch0120:            0120-units-add-Install-section-to-tmp.mount.patch
Patch0121:            0121-nss-do-not-modify-errno-when-NSS_STATUS_NOTFOUND-or-.patch
Patch0122:            0122-util.h-add-new-UNPROTECT_ERRNO-macro.patch
Patch0123:            0123-nss-unportect-errno-before-writing-to-NSS-errnop.patch
Patch0124:            0124-seccomp-reduce-logging-about-failure-to-add-syscall-.patch
Patch0125:            0125-format-table-when-duplicating-a-cell-also-copy-the-c.patch
Patch0126:            0126-format-table-optionally-make-specific-cells-clickabl.patch
Patch0127:            0127-format-table-before-outputting-a-color-check-if-colo.patch
Patch0128:            0128-format-table-add-option-to-store-format-percent-and-.patch
Patch0129:            0129-format-table-optionally-allow-reversing-the-sort-ord.patch
Patch0130:            0130-format-table-add-table_update-to-update-existing-ent.patch
Patch0131:            0131-format-table-add-an-API-for-getting-the-cell-at-a-sp.patch
Patch0132:            0132-format-table-always-underline-header-line.patch
Patch0133:            0133-format-table-add-calls-to-query-the-data-in-a-specif.patch
Patch0134:            0134-format-table-make-sure-we-never-call-memcmp-with-NUL.patch
Patch0135:            0135-format-table-use-right-field-for-display.patch
Patch0136:            0136-format-table-add-option-to-uppercase-cells-on-displa.patch
Patch0137:            0137-format-table-never-try-to-reuse-cells-that-have-colo.patch
Patch0138:            0138-locale-util-add-logic-to-output-smiley-emojis-at-var.patch
Patch0139:            0139-analyze-add-new-security-verb.patch
Patch0140:            0140-tests-add-a-rudimentary-fuzzer-for-server_process_sy.patch
Patch0141:            0141-journald-make-it-clear-that-dev_kmsg_record-modifies.patch
Patch0142:            0142-journald-free-the-allocated-memory-before-returning-.patch
Patch0143:            0143-tests-rework-the-code-fuzzing-journald.patch
Patch0144:            0144-journald-make-server_process_native_message-compatib.patch
Patch0145:            0145-tests-add-a-fuzzer-for-server_process_native_message.patch
Patch0146:            0146-tests-add-a-fuzzer-for-sd-ndisc.patch
Patch0147:            0147-ndisc-fix-two-infinite-loops.patch
Patch0148:            0148-tests-add-reproducers-for-several-issues-uncovered-w.patch
Patch0149:            0149-tests-add-a-reproducer-for-an-infinite-loop-in-ndisc.patch
Patch0150:            0150-tests-add-a-reproducer-for-another-infinite-loop-in-.patch
Patch0151:            0151-fuzz-rename-fuzz-corpus-directory-to-just-fuzz.patch
Patch0152:            0152-test-add-testcase-for-issue-10007-by-oss-fuzz.patch
Patch0153:            0153-fuzz-unify-the-fuzz-regressions-directory-with-the-m.patch
Patch0154:            0154-test-bus-marshal-use-cescaping-instead-of-hexmem.patch
Patch0155:            0155-meson-add-Dlog-trace-to-set-LOG_TRACE.patch
Patch0156:            0156-meson-allow-building-resolved-and-machined-without-n.patch
Patch0157:            0157-meson-drop-duplicated-condition.patch
Patch0158:            0158-meson-use-.source_root-in-more-places.patch
Patch0159:            0159-meson-treat-all-fuzz-cases-as-unit-tests.patch
Patch0160:            0160-fuzz-bus-message-add-fuzzer-for-message-parsing.patch
Patch0161:            0161-bus-message-use-structured-initialization-to-avoid-u.patch
Patch0162:            0162-bus-message-avoid-an-infinite-loop-on-empty-structur.patch
Patch0163:            0163-bus-message-let-s-always-use-EBADMSG-when-the-messag.patch
Patch0164:            0164-bus-message-rename-function-for-clarity.patch
Patch0165:            0165-bus-message-use-define.patch
Patch0166:            0166-bus-do-not-print-null-if-the-message-has-unknown-typ.patch
Patch0167:            0167-bus-message-fix-calculation-of-offsets-table.patch
Patch0168:            0168-bus-message-remove-duplicate-assignment.patch
Patch0169:            0169-bus-message-fix-calculation-of-offsets-table-for-arr.patch
Patch0170:            0170-bus-message-drop-asserts-in-functions-which-are-wrap.patch
Patch0171:            0171-bus-message-output-debug-information-about-offset-tr.patch
Patch0172:            0172-bus-message-fix-skipping-of-array-fields-in-gvariant.patch
Patch0173:            0173-bus-message-also-properly-copy-struct-signature-when.patch
Patch0174:            0174-fuzz-bus-message-add-two-test-cases-that-pass-now.patch
Patch0175:            0175-bus-message-return-EBADMSG-not-EINVAL-on-invalid-gva.patch
Patch0176:            0176-bus-message-avoid-wrap-around-when-using-length-read.patch
Patch0177:            0177-util-do-not-use-stack-frame-for-parsing-arbitrary-in.patch
Patch0178:            0178-travis-enable-ASan-and-UBSan-on-RHEL8.patch
Patch0179:            0179-tests-keep-SYS_PTRACE-when-running-under-ASan.patch
Patch0180:            0180-tree-wide-various-ubsan-zero-size-memory-fixes.patch
Patch0181:            0181-util-introduce-memcmp_safe.patch
Patch0182:            0182-test-socket-util-avoid-memleak-reported-by-valgrind.patch
Patch0183:            0183-sd-journal-escape-binary-data-in-match_make_string.patch
Patch0184:            0184-capability-introduce-CAP_TO_MASK_CORRECTED-macro-rep.patch
Patch0185:            0185-sd-bus-use-size_t-when-dealing-with-memory-offsets.patch
Patch0186:            0186-sd-bus-call-cap_last_cap-only-once-in-has_cap.patch
Patch0187:            0187-mount-point-honour-AT_SYMLINK_FOLLOW-correctly.patch
Patch0188:            0188-travis-switch-from-trusty-to-xenial.patch
Patch0189:            0189-test-socket-util-Add-tests-for-receive_fd_iov-and-fr.patch
Patch0190:            0190-socket-util-Introduce-send_one_fd_iov-and-receive_on.patch
Patch0191:            0191-core-swap-order-of-n_storage_fds-and-n_socket_fds-pa.patch
Patch0192:            0192-execute-use-our-usual-syntax-for-defining-bit-masks.patch
Patch0193:            0193-core-introduce-new-Type-exec-service-type.patch
Patch0194:            0194-man-document-the-new-Type-exec-type.patch
Patch0195:            0195-sd-bus-allow-connecting-to-the-pseudo-container-.hos.patch
Patch0196:            0196-sd-login-let-s-also-make-sd-login-understand-.host.patch
Patch0197:            0197-test-add-test-for-Type-exec.patch
Patch0198:            0198-journal-gateway-explicitly-declare-local-variables.patch
Patch0199:            0199-tools-drop-unused-variable.patch
Patch0200:            0200-journal-gateway-use-localStorage-cursor-only-when-it.patch
Patch0201:            0201-sd-bus-deal-with-cookie-overruns.patch
Patch0202:            0202-journal-remote-do-not-request-Content-Length-if-Tran.patch
Patch0203:            0203-journal-do-not-remove-multiple-spaces-after-identifi.patch
Patch0204:            0204-cryptsetup-Do-not-fallback-to-PLAIN-mapping-if-LUKS-.patch
Patch0205:            0205-cryptsetup-call-crypt_load-for-LUKS-only-once.patch
Patch0206:            0206-cryptsetup-Add-LUKS2-token-support.patch
Patch0207:            0207-udev-scsi_id-fix-incorrect-page-length-when-get-devi.patch
Patch0208:            0208-Change-job-mode-of-manager-triggered-restarts-to-JOB.patch
Patch0209:            0209-bash-completion-analyze-support-security.patch
Patch0210:            0210-man-note-that-journal-does-not-validate-syslog-field.patch
Patch0211:            0211-rules-skip-memory-hotplug-on-ppc64.patch
Patch0212:            0212-mount-simplify-proc-self-mountinfo-handler.patch
Patch0213:            0213-mount-rescan-proc-self-mountinfo-before-processing-w.patch
Patch0214:            0214-swap-scan-proc-swaps-before-processing-waitid-result.patch
Patch0215:            0215-analyze-security-fix-potential-division-by-zero.patch
Patch0216:            0216-core-never-propagate-reload-failure-to-service-resul.patch
Patch0217:            0217-man-document-systemd-analyze-security.patch
Patch0218:            0218-man-reorder-and-add-examples-to-systemd-analyze-1.patch
Patch0219:            0219-travis-move-to-CentOS-8-docker-images.patch
Patch0220:            0220-travis-drop-SCL-remains.patch
Patch0221:            0221-syslog-fix-segfault-in-syslog_parse_priority.patch
Patch0222:            0222-sd-bus-make-strict-asan-shut-up.patch
Patch0223:            0223-travis-don-t-run-slow-tests-under-ASan-UBSan.patch
Patch0224:            0224-kernel-install-do-not-require-non-empty-kernel-cmdli.patch
Patch0225:            0225-ask-password-prevent-buffer-overrow-when-reading-fro.patch
Patch0226:            0226-core-try-to-reopen-dev-kmsg-again-right-after-mounti.patch
Patch0227:            0227-buildsys-don-t-garbage-collect-sections-while-linkin.patch
Patch0228:            0228-udev-introduce-CONST-key-name.patch
Patch0229:            0229-Call-getgroups-to-know-size-of-supplementary-groups-.patch
Patch0230:            0230-Consider-smb3-as-remote-filesystem.patch
Patch0231:            0231-process-util-introduce-pid_is_my_child-helper.patch
Patch0232:            0232-core-reduce-the-number-of-stalled-PIDs-from-the-watc.patch
Patch0233:            0233-core-only-watch-processes-when-it-s-really-necessary.patch
Patch0234:            0234-core-implement-per-unit-journal-rate-limiting.patch
Patch0235:            0235-path-stop-watching-path-specs-once-we-triggered-the-.patch
Patch0236:            0236-journald-fixed-assertion-failure-when-system-journal.patch
Patch0237:            0237-test-use-PBKDF2-instead-of-Argon2-in-cryptsetup.patch
Patch0238:            0238-test-mask-several-unnecessary-services.patch
Patch0239:            0239-test-bump-the-second-partition-s-size-to-50M.patch
Patch0240:            0240-shared-sleep-config-exclude-zram-devices-from-hibern.patch
Patch0241:            0241-selinux-don-t-log-SELINUX_INFO-and-SELINUX_WARNING-m.patch
Patch0242:            0242-sd-device-introduce-log_device_-macros.patch
Patch0243:            0243-udev-Add-id-program-and-rule-for-FIDO-security-token.patch
Patch0244:            0244-shared-but-util-drop-trusted-annotation-from-bus_ope.patch
Patch0245:            0245-sd-bus-adjust-indentation-of-comments.patch
Patch0246:            0246-resolved-do-not-run-loop-twice.patch
Patch0247:            0247-resolved-allow-access-to-Set-Link-and-Revert-methods.patch
Patch0248:            0248-resolved-query-polkit-only-after-parsing-the-data.patch
Patch0249:            0249-journal-rely-on-_cleanup_free_-to-free-a-temporary-s.patch
Patch0250:            0250-basic-user-util-allow-dots-in-user-names.patch
Patch0251:            0251-sd-bus-bump-message-queue-size-again.patch
Patch0252:            0252-tests-put-fuzz_journald_processing_function-in-a-.c-.patch
Patch0253:            0253-tests-add-a-fuzzer-for-dev_kmsg_record.patch
Patch0254:            0254-basic-remove-an-assertion-from-cunescape_one.patch
Patch0255:            0255-journal-fix-an-off-by-one-error-in-dev_kmsg_record.patch
Patch0256:            0256-tests-add-a-reproducer-for-a-memory-leak-fixed-in-30.patch
Patch0257:            0257-tests-add-a-reproducer-for-a-heap-buffer-overflow-fi.patch
Patch0258:            0258-test-initialize-syslog_fd-in-fuzz-journald-kmsg-too.patch
Patch0259:            0259-tests-add-a-fuzzer-for-process_audit_string.patch
Patch0260:            0260-journald-check-whether-sscanf-has-changed-the-value-.patch
Patch0261:            0261-tests-introduce-dummy_server_init-and-use-it-in-all-.patch
Patch0262:            0262-tests-add-a-fuzzer-for-journald-streams.patch
Patch0263:            0263-tests-add-a-fuzzer-for-server_process_native_file.patch
Patch0264:            0264-fuzz-journal-stream-avoid-assertion-failure-on-sampl.patch
Patch0265:            0265-journald-take-leading-spaces-into-account-in-syslog_.patch
Patch0266:            0266-Add-a-warning-about-the-difference-in-permissions-be.patch
Patch0267:            0267-execute-remove-one-redundant-comparison-check.patch
Patch0268:            0268-core-change-ownership-mode-of-the-execution-director.patch
Patch0269:            0269-core-dbus-execute-remove-unnecessary-initialization.patch
Patch0270:            0270-shared-cpu-set-util-move-the-part-to-print-cpu-set-i.patch
Patch0271:            0271-shared-cpu-set-util-remove-now-unused-CPU_SIZE_TO_NU.patch
Patch0272:            0272-Rework-cpu-affinity-parsing.patch
Patch0273:            0273-Move-cpus_in_affinity_mask-to-cpu-set-util.-ch.patch
Patch0274:            0274-test-cpu-set-util-add-simple-test-for-cpus_in_affini.patch
Patch0275:            0275-test-cpu-set-util-add-a-smoke-test-for-test_parse_cp.patch
Patch0276:            0276-pid1-parse-CPUAffinity-in-incremental-fashion.patch
Patch0277:            0277-pid1-don-t-reset-setting-from-proc-cmdline-upon-rest.patch
Patch0278:            0278-pid1-when-reloading-configuration-forget-old-setting.patch
Patch0279:            0279-test-execute-use-CPUSet-too.patch
Patch0280:            0280-shared-cpu-set-util-drop-now-unused-cleanup-function.patch
Patch0281:            0281-shared-cpu-set-util-make-transfer-of-cpu_set_t-over-.patch
Patch0282:            0282-test-cpu-set-util-add-test-for-dbus-conversions.patch
Patch0283:            0283-shared-cpu-set-util-introduce-cpu_set_to_range.patch
Patch0284:            0284-systemctl-present-CPUAffinity-mask-as-a-list-of-CPU-.patch
Patch0285:            0285-shared-cpu-set-util-only-force-range-printing-one-ti.patch
Patch0286:            0286-execute-dump-CPUAffinity-as-a-range-string-instead-o.patch
Patch0287:            0287-cpu-set-util-use-d-d-format-in-cpu_set_to_range_stri.patch
Patch0288:            0288-core-introduce-NUMAPolicy-and-NUMAMask-options.patch
Patch0289:            0289-core-disable-CPUAccounting-by-default.patch
Patch0290:            0290-set-kptr_restrict-1.patch
Patch0291:            0291-cryptsetup-reduce-the-chance-that-we-will-be-OOM-kil.patch
Patch0292:            0292-core-job-fix-breakage-of-ordering-dependencies-by-sy.patch
Patch0293:            0293-debug-generator-enable-custom-systemd.debug_shell-tt.patch
Patch0294:            0294-test-cpu-set-util-fix-comparison-for-allocation-size.patch
Patch0295:            0295-test-cpu-set-util-fix-allocation-size-check-on-i386.patch
Patch0296:            0296-catalog-fix-name-of-variable.patch
Patch0297:            0297-cryptsetup-add-keyfile-timeout-to-allow-a-keydev-tim.patch
Patch0298:            0298-cryptsetup-add-documentation-for-keyfile-timeout.patch
Patch0299:            0299-cryptsetup-use-unabbrieviated-variable-names.patch
Patch0300:            0300-cryptsetup-don-t-assert-on-variable-which-is-optiona.patch
Patch0301:            0301-cryptsetup-generator-guess-whether-the-keyfile-argum.patch
Patch0302:            0302-crypt-util-Translate-libcryptsetup-log-level-instead.patch
Patch0303:            0303-cryptsetup-add-some-commenting-about-EAGAIN-generati.patch
Patch0304:            0304-cryptsetup-downgrade-a-log-message-we-ignore.patch
Patch0305:            0305-cryptsetup-rework-how-we-log-about-activation-failur.patch
Patch0306:            0306-rules-reintroduce-60-alias-kmsg.rules.patch
Patch0307:            0307-sd-bus-make-rqueue-wqueue-sizes-of-type-size_t.patch
Patch0308:            0308-sd-bus-reorder-bus-ref-and-bus-message-ref-handling.patch
Patch0309:            0309-sd-bus-make-sure-dispatch_rqueue-initializes-return-.patch
Patch0310:            0310-sd-bus-drop-two-inappropriate-empty-lines.patch
Patch0311:            0311-sd-bus-initialize-mutex-after-we-allocated-the-wqueu.patch
Patch0312:            0312-sd-bus-always-go-through-sd_bus_unref-to-free-messag.patch
Patch0313:            0313-bus-message-introduce-two-kinds-of-references-to-bus.patch
Patch0314:            0314-sd-bus-introduce-API-for-re-enqueuing-incoming-messa.patch
Patch0315:            0315-sd-event-add-sd_event_source_disable_unref-helper.patch
Patch0316:            0316-polkit-when-authorizing-via-PK-let-s-re-resolve-call.patch
Patch0317:            0317-sysctl-let-s-by-default-increase-the-numeric-PID-ran.patch
Patch0318:            0318-journal-do-not-trigger-assertion-when-journal_file_c.patch
Patch0319:            0319-journal-use-cleanup-attribute-at-one-more-place.patch
Patch0320:            0320-sd-bus-use-queue-message-references-for-managing-r-w.patch
Patch0321:            0321-pid1-make-sure-to-restore-correct-default-values-for.patch
Patch0322:            0322-main-introduce-a-define-HIGH_RLIMIT_MEMLOCK-similar-.patch
Patch0323:            0323-seccomp-introduce-seccomp_restrict_suid_sgid-for-blo.patch
Patch0324:            0324-test-add-test-case-for-restrict_suid_sgid.patch
Patch0325:            0325-core-expose-SUID-SGID-restriction-as-new-unit-settin.patch
Patch0326:            0326-analyze-check-for-RestrictSUIDSGID-in-systemd-analyz.patch
Patch0327:            0327-man-document-the-new-RestrictSUIDSGID-setting.patch
Patch0328:            0328-units-turn-on-RestrictSUIDSGID-in-most-of-our-long-r.patch
Patch0329:            0329-core-imply-NNP-and-SUID-SGID-restriction-for-Dynamic.patch
Patch0330:            0330-cgroup-introduce-support-for-cgroup-v2-CPUSET-contro.patch
Patch0331:            0331-pid1-fix-DefaultTasksMax-initialization.patch
Patch0332:            0332-cgroup-make-sure-that-cpuset-is-supported-on-cgroup-.patch
Patch0333:            0333-test-introduce-TEST-36-NUMAPOLICY.patch
Patch0334:            0334-test-replace-tail-f-with-journal-cursor-which-should.patch
Patch0335:            0335-test-support-MPOL_LOCAL-matching-in-unpatched-strace.patch
Patch0336:            0336-test-make-sure-the-strace-process-is-indeed-dead.patch
Patch0337:            0337-test-skip-the-test-on-systems-without-NUMA-support.patch
Patch0338:            0338-test-give-strace-some-time-to-initialize.patch
Patch0339:            0339-test-add-a-simple-sanity-check-for-systems-without-N.patch
Patch0340:            0340-test-drop-the-missed-exit-1-expression.patch
Patch0341:            0341-test-replace-cursor-file-with-a-plain-cursor.patch
Patch0342:            0342-cryptsetup-Treat-key-file-errors-as-a-failed-passwor.patch
Patch0343:            0343-swap-finish-the-secondary-swap-units-jobs-if-deactiv.patch
Patch0344:            0344-resolved-Recover-missing-PrivateTmp-yes-and-ProtectS.patch
Patch0345:            0345-bus_open-leak-sd_event_source-when-udevadm-trigger.patch
Patch0346:            0346-core-rework-StopWhenUnneeded-logic.patch
Patch0347:            0347-pid1-fix-the-names-of-AllowedCPUs-and-AllowedMemoryN.patch
Patch0348:            0348-core-fix-re-realization-of-cgroup-siblings.patch
Patch0349:            0349-basic-use-comma-as-separator-in-cpuset-cgroup-cpu-ra.patch
Patch0350:            0350-core-transition-to-FINAL_SIGTERM-state-after-ExecSto.patch
Patch0351:            0351-sd-journal-close-journal-files-that-were-deleted-by-.patch
Patch0352:            0352-sd-journal-remove-the-dead-code-and-actually-fix-146.patch
Patch0353:            0353-udev-downgrade-message-when-we-fail-to-set-inotify-w.patch
Patch0354:            0354-logind-check-PolicyKit-before-allowing-VT-switch.patch
Patch0355:            0355-test-do-not-use-global-variable-to-pass-error.patch
Patch0356:            0356-test-install-libraries-required-by-tests.patch
Patch0357:            0357-test-introduce-install_zoneinfo.patch
Patch0358:            0358-test-replace-duplicated-Makefile-by-symbolic-link.patch
Patch0359:            0359-test-add-paths-of-keymaps-in-install_keymaps.patch
Patch0360:            0360-test-make-install_keymaps-optionally-install-more-ke.patch
Patch0361:            0361-test-fs-util-skip-some-tests-when-running-in-unprivi.patch
Patch0362:            0362-test-process-util-skip-several-verifications-when-ru.patch
Patch0363:            0363-test-execute-also-check-python3-is-installed-or-not.patch
Patch0364:            0364-test-execute-skip-several-tests-when-running-in-cont.patch
Patch0365:            0365-test-introduce-test_is_running_from_builddir.patch
Patch0366:            0366-test-make-test-catalog-relocatable.patch
Patch0367:            0367-test-parallelize-tasks-in-TEST-24-UNIT-TESTS.patch
Patch0368:            0368-test-try-to-determine-QEMU_SMP-dynamically.patch
Patch0369:            0369-test-store-coredumps-in-journal.patch
Patch0370:            0370-pid1-add-new-kernel-cmdline-arg-systemd.cpu_affinity.patch
Patch0371:            0371-udev-rules-make-tape-changers-also-apprear-in-dev-ta.patch
Patch0372:            0372-man-be-clearer-that-.timer-time-expressions-need-to-.patch
Patch0373:            0373-Add-support-for-opening-files-for-appending.patch
Patch0374:            0374-nspawn-move-payload-to-sub-cgroup-first-then-sync-cg.patch
Patch0375:            0375-nspawn-chown-the-legacy-hierarchy-when-it-s-used-in-.patch
Patch0376:            0376-core-move-unit_status_emit_starting_stopping_reloadi.patch
Patch0377:            0377-job-when-a-job-was-skipped-due-to-a-failed-condition.patch
Patch0378:            0378-core-split-out-all-logic-that-updates-a-Job-on-a-uni.patch
Patch0379:            0379-core-make-log-messages-about-units-entering-a-failed.patch
Patch0380:            0380-core-log-a-recognizable-message-when-a-unit-succeeds.patch
Patch0381:            0381-tests-always-use-the-right-vtable-wrapper-calls.patch
Patch0382:            0382-test-execute-allow-filtering-test-cases-by-pattern.patch
Patch0383:            0383-test-execute-provide-custom-failure-message.patch
Patch0384:            0384-core-ExecCondition-for-services.patch
Patch0385:            0385-Drop-support-for-lz4-1.3.0.patch
Patch0386:            0386-test-compress-add-test-for-short-decompress_startswi.patch
Patch0387:            0387-journal-adapt-for-new-improved-LZ4_decompress_safe_p.patch
Patch0388:            0388-fuzz-compress-add-fuzzer-for-compression-and-decompr.patch
Patch0389:            0389-seccomp-fix-__NR__sysctl-usage.patch
Patch0390:            0390-tmpfiles-fix-crash-with-NULL-in-arg_root-and-other-f.patch
Patch0391:            0391-sulogin-shell-Use-force-if-SYSTEMD_SULOGIN_FORCE-set.patch
Patch0392:            0392-resolvconf-fixes-for-the-compatibility-interface.patch
Patch0393:            0393-mount-don-t-add-Requires-for-tmp.mount.patch
Patch0394:            0394-core-coldplug-possible-nop_job.patch
Patch0395:            0395-core-add-IODeviceLatencyTargetSec.patch
Patch0396:            0396-time-util-Introduce-parse_sec_def_infinity.patch
Patch0397:            0397-cgroup-use-structured-initialization.patch
Patch0398:            0398-core-add-CPUQuotaPeriodSec.patch
Patch0399:            0399-core-downgrade-CPUQuotaPeriodSec-clamping-logs-to-de.patch
Patch0400:            0400-sd-bus-avoid-magic-number-in-SASL-length-calculation.patch
Patch0401:            0401-sd-bus-fix-SASL-reply-to-empty-AUTH.patch
Patch0402:            0402-sd-bus-skip-sending-formatted-UIDs-via-SASL.patch
Patch0403:            0403-core-add-MemoryMin.patch
Patch0404:            0404-core-introduce-cgroup_add_device_allow.patch
Patch0405:            0405-test-remove-support-for-suffix-in-get_testdata_dir.patch
Patch0406:            0406-cgroup-Implement-default-propagation-of-MemoryLow-wi.patch
Patch0407:            0407-cgroup-Create-UNIT_DEFINE_ANCESTOR_MEMORY_LOOKUP.patch
Patch0408:            0408-unit-Add-DefaultMemoryMin.patch
Patch0409:            0409-cgroup-Polish-hierarchically-aware-protection-docs-a.patch
Patch0410:            0410-cgroup-Readd-some-plumbing-for-DefaultMemoryMin.patch
Patch0411:            0411-cgroup-Support-0-value-for-memory-protection-directi.patch
Patch0412:            0412-cgroup-Test-that-it-s-possible-to-set-memory-protect.patch
Patch0413:            0413-cgroup-Check-ancestor-memory-min-for-unified-memory-.patch
Patch0414:            0414-cgroup-Respect-DefaultMemoryMin-when-setting-memory..patch
Patch0415:            0415-cgroup-Mark-memory-protections-as-explicitly-set-in-.patch
Patch0416:            0416-meson-allow-setting-the-version-string-during-config.patch
Patch0417:            0417-core-don-t-consider-SERVICE_SKIP_CONDITION-for-abnor.patch
Patch0418:            0418-selinux-do-preprocessor-check-only-in-selinux-access.patch
Patch0419:            0419-basic-cgroup-util-introduce-cg_get_keyed_attribute_f.patch
Patch0420:            0420-shared-add-generic-logic-for-waiting-for-a-unit-to-e.patch
Patch0421:            0421-shared-fix-assert-call.patch
Patch0422:            0422-shared-Don-t-try-calling-NULL-callback-in-bus_wait_f.patch
Patch0423:            0423-shared-add-NULL-callback-check-in-one-more-place.patch
Patch0424:            0424-core-introduce-support-for-cgroup-freezer.patch
Patch0425:            0425-core-cgroup-fix-return-value-of-unit_cgorup_freezer_.patch
Patch0426:            0426-core-fix-the-return-value-in-order-to-make-sure-we-d.patch
Patch0427:            0427-test-add-test-for-cgroup-v2-freezer-support.patch
Patch0428:            0428-fix-mis-merge.patch
Patch0429:            0429-tests-sleep-a-bit-and-give-kernel-time-to-perform-th.patch
Patch0430:            0430-device-make-sure-we-emit-PropertiesChanged-signal-on.patch
Patch0431:            0431-device-don-t-emit-PropetiesChanged-needlessly.patch
Patch0432:            0432-units-add-generic-boot-complete.target.patch
Patch0433:            0433-man-document-new-boot-complete.target-unit.patch
Patch0434:            0434-core-make-sure-to-restore-the-control-command-id-too.patch
Patch0435:            0435-cgroup-freezer-action-must-be-NOP-when-cgroup-v2-fre.patch
Patch0436:            0436-logind-don-t-print-warning-when-user-.service-templa.patch
Patch0437:            0437-build-use-simple-project-version-in-pkgconfig-files.patch
Patch0438:            0438-basic-virt-try-the-proc-1-sched-hack-also-for-PID1.patch
Patch0439:            0439-seccomp-rework-how-the-S-UG-ID-filter-is-installed.patch
Patch0440:            0440-vconsole-setup-downgrade-log-message-when-setting-fo.patch
Patch0441:            0441-units-fix-systemd.special-man-page-reference-in-syst.patch
Patch0442:            0442-units-drop-reference-to-sushell-man-page.patch
Patch0443:            0443-sd-bus-break-the-loop-in-bus_ensure_running-if-the-b.patch
Patch0444:            0444-core-add-new-API-for-enqueing-a-job-with-returning-t.patch
Patch0445:            0445-systemctl-replace-switch-statement-by-table-of-struc.patch
Patch0446:            0446-systemctl-reindent-table.patch
Patch0447:            0447-systemctl-Only-wait-when-there-s-something-to-wait-f.patch
Patch0448:            0448-systemctl-clean-up-start_unit_one-error-handling.patch
Patch0449:            0449-systemctl-split-out-extra-args-generation-into-helpe.patch
Patch0450:            0450-systemctl-add-new-show-transaction-switch.patch
Patch0451:            0451-test-add-some-basic-testing-that-systemctl-start-T-d.patch
Patch0452:            0452-man-document-the-new-systemctl-show-transaction-opti.patch
Patch0453:            0453-socket-New-option-FlushPending-boolean-to-flush-sock.patch
Patch0454:            0454-core-remove-support-for-API-bus-started-outside-our-.patch
Patch0455:            0455-mount-setup-fix-segfault-in-mount_cgroup_controllers.patch
Patch0456:            0456-dbus-execute-make-transfer-of-CPUAffinity-endian-saf.patch
Patch0457:            0457-core-add-support-for-setting-CPUAffinity-to-special-.patch
Patch0458:            0458-basic-user-util-always-use-base-10-for-user-group-nu.patch
Patch0459:            0459-parse-util-sometimes-it-is-useful-to-check-if-a-stri.patch
Patch0460:            0460-basic-parse-util-add-safe_atoux64.patch
Patch0461:            0461-parse-util-allow-tweaking-how-to-parse-integers.patch
Patch0462:            0462-parse-util-allow-0-as-alternative-to-0-and-0.patch
Patch0463:            0463-parse-util-make-return-parameter-optional-in-safe_at.patch
Patch0464:            0464-parse-util-rewrite-parse_mode-on-top-of-safe_atou_fu.patch
Patch0465:            0465-user-util-be-stricter-in-parse_uid.patch
Patch0466:            0466-strv-add-new-macro-STARTSWITH_SET.patch
Patch0467:            0467-parse-util-also-parse-integers-prefixed-with-0b-and-.patch
Patch0468:            0468-tests-beef-up-integer-parsing-tests.patch
Patch0469:            0469-shared-user-util-add-compat-forms-of-user-name-check.patch
Patch0470:            0470-shared-user-util-emit-a-warning-on-names-with-dots.patch
Patch0471:            0471-user-util-Allow-names-starting-with-a-digit.patch
Patch0472:            0472-shared-user-util-allow-usernames-with-dots-in-specif.patch
Patch0473:            0473-user-util-switch-order-of-checks-in-valid_user_group.patch
Patch0474:            0474-user-util-rework-how-we-validate-user-names.patch
Patch0475:            0475-man-mention-System-Administrator-s-Guide-in-systemct.patch
Patch0476:            0476-udev-introduce-udev-net_id-naming-schemes.patch
Patch0477:            0477-meson-make-net.naming-scheme-default-configurable.patch
Patch0478:            0478-man-describe-naming-schemes-in-a-new-man-page.patch
Patch0479:            0479-udev-net_id-parse-_SUN-ACPI-index-as-a-signed-intege.patch
Patch0480:            0480-udev-net_id-don-t-generate-slot-based-names-if-multi.patch
Patch0481:            0481-fix-typo-in-ProtectSystem-option.patch
Patch0482:            0482-remove-references-of-non-existent-man-pages.patch
Patch0483:            0483-log-Prefer-logging-to-CLI-unless-JOURNAL_STREAM-is-s.patch
Patch0484:            0484-locale-util-add-new-helper-locale_is_installed.patch
Patch0485:            0485-test-add-test-case-for-locale_is_installed.patch
Patch0486:            0486-tree-wide-port-various-bits-over-to-locale_is_instal.patch
Patch0487:            0487-install-allow-instantiated-units-to-be-enabled-via-p.patch
Patch0488:            0488-install-small-refactor-to-combine-two-function-calls.patch
Patch0489:            0489-test-fix-a-memleak.patch
Patch0490:            0490-docs-Add-syntax-for-templated-units-to-systemd.prese.patch
Patch0491:            0491-shared-install-fix-preset-operations-for-non-service.patch
Patch0492:            0492-introduce-setsockopt_int-helper.patch
Patch0493:            0493-socket-util-add-generic-socket_pass_pktinfo-helper.patch
Patch0494:            0494-core-add-new-PassPacketInfo-socket-unit-property.patch
Patch0495:            0495-resolved-tweak-cmsg-calculation.patch
Patch0496:            0496-ci-PowerTools-repo-was-renamed-to-powertools-in-RHEL.patch
Patch0497:            0497-ci-use-quay.io-instead-of-Docker-Hub-to-avoid-rate-l.patch
Patch0498:            0498-ci-move-jobs-from-Travis-CI-to-GH-Actions.patch
Patch0499:            0499-unit-make-UNIT-cast-function-deal-with-NULL-pointers.patch
Patch0500:            0500-use-link-to-RHEL-8-docs.patch
Patch0501:            0501-cgroup-Also-set-blkio.bfq.weight.patch
Patch0502:            0502-units-make-sure-initrd-cleanup.service-terminates-be.patch
Patch0503:            0503-core-reload-SELinux-label-cache-on-daemon-reload.patch
Patch0504:            0504-selinux-introduce-mac_selinux_create_file_prepare_at.patch
Patch0505:            0505-selinux-add-trigger-for-policy-reload-to-refresh-int.patch
Patch0506:            0506-udev-net_id-give-RHEL-8.4-naming-scheme-a-name.patch
Patch0507:            0507-basic-stat-util-make-mtime-check-stricter-and-use-en.patch
Patch0508:            0508-udev-make-algorithm-that-selects-highest-priority-de.patch
Patch0509:            0509-test-create-dev-null-in-test-udev.pl.patch
Patch0510:            0510-test-missing-die.patch
Patch0511:            0511-udev-test-remove-a-check-for-whether-the-test-is-run.patch
Patch0512:            0512-udev-test-skip-the-test-only-if-it-can-t-setup-its-e.patch
Patch0513:            0513-udev-test-fix-test-skip-condition.patch
Patch0514:            0514-udev-test-fix-missing-directory-test-run.patch
Patch0515:            0515-udev-test-check-if-permitted-to-create-block-device-.patch
Patch0516:            0516-test-udev-add-a-testcase-of-too-long-line.patch
Patch0517:            0517-test-udev-use-proper-semantics-for-too-long-line-wit.patch
Patch0518:            0518-test-udev-add-more-tests-for-line-continuations-and-.patch
Patch0519:            0519-test-udev-add-more-tests-for-line-continuation.patch
Patch0520:            0520-test-udev-fix-alignment-and-drop-unnecessary-white-s.patch
Patch0521:            0521-test-udev-test.pl-cleanup-if-skipping-test.patch
Patch0522:            0522-test-add-test-cases-for-empty-string-match.patch
Patch0523:            0523-test-add-test-case-for-multi-matches-when-use.patch
Patch0524:            0524-udev-test-do-not-rely-on-mail-group-being-defined.patch
Patch0525:            0525-test-udev-test.pl-allow-multiple-devices-per-test.patch
Patch0526:            0526-test-udev-test.pl-create-rules-only-once.patch
Patch0527:            0527-test-udev-test.pl-allow-concurrent-additions-and-rem.patch
Patch0528:            0528-test-udev-test.pl-use-computed-devnode-name.patch
Patch0529:            0529-test-udev-test.pl-test-correctness-of-symlink-target.patch
Patch0530:            0530-test-udev-test.pl-allow-checking-multiple-symlinks.patch
Patch0531:            0531-test-udev-test.pl-fix-wrong-test-descriptions.patch
Patch0532:            0532-test-udev-test.pl-last_rule-is-unsupported.patch
Patch0533:            0533-test-udev-test.pl-Make-some-tests-a-little-harder.patch
Patch0534:            0534-test-udev-test.pl-remove-bogus-rules-from-magic-subs.patch
Patch0535:            0535-test-udev-test.pl-merge-space-and-var-with-space-tes.patch
Patch0536:            0536-test-udev-test.pl-merge-import-parent-tests-into-one.patch
Patch0537:            0537-test-udev-test.pl-count-good-results.patch
Patch0538:            0538-tests-udev-test.pl-add-multiple-device-test.patch
Patch0539:            0539-test-udev-test.pl-add-repeat-count.patch
Patch0540:            0540-test-udev-test.pl-generator-for-large-list-of-block-.patch
Patch0541:            0541-test-udev-test.pl-suppress-umount-error-message-at-s.patch
Patch0542:            0542-test-udev_test.pl-add-expected-good-count.patch
Patch0543:            0543-test-udev-test-gracefully-exit-when-imports-fail.patch
Patch0544:            0544-Revert-test-add-test-cases-for-empty-string-match-an.patch
Patch0545:            0545-test-sys-script.py-add-missing-DEVNAME-entries-to-ue.patch
Patch0546:            0546-sd-event-split-out-helper-functions-for-reshuffling-.patch
Patch0547:            0547-sd-event-split-out-enable-and-disable-codepaths-from.patch
Patch0548:            0548-sd-event-mention-that-two-debug-logged-events-are-ig.patch
Patch0549:            0549-sd-event-split-clock-data-allocation-out-of-sd_event.patch
Patch0550:            0550-sd-event-split-out-code-to-add-remove-timer-event-so.patch
Patch0551:            0551-sd-event-fix-delays-assert-brain-o-17790.patch
Patch0552:            0552-sd-event-let-s-suffix-last_run-last_log-with-_usec.patch
Patch0553:            0553-sd-event-refuse-running-default-event-loops-in-any-o.patch
Patch0554:            0554-sd-event-ref-event-loop-while-in-sd_event_prepare-ot.patch
Patch0555:            0555-sd-event-follow-coding-style-with-naming-return-para.patch
Patch0556:            0556-sd-event-remove-earliest_index-latest_index-into-com.patch
Patch0557:            0557-sd-event-update-state-at-the-end-in-event_source_ena.patch
Patch0558:            0558-sd-event-increase-n_enabled_child_sources-just-once.patch
Patch0559:            0559-sd-event-add-ability-to-ratelimit-event-sources.patch
Patch0560:            0560-test-add-ratelimiting-test.patch
Patch0561:            0561-core-prevent-excessive-proc-self-mountinfo-parsing.patch
Patch0562:            0562-udev-run-link_update-with-increased-retry-count-in-s.patch
Patch0563:            0563-pam-systemd-use-secure_getenv-rather-than-getenv.patch
Patch0564:            0564-Revert-udev-run-link_update-with-increased-retry-cou.patch
Patch0565:            0565-Revert-udev-make-algorithm-that-selects-highest-prio.patch
Patch0566:            0566-test-udev-test.pl-drop-test-cases-that-add-mutliple-.patch
Patch0567:            0567-cgroup-Also-set-io.bfq.weight.patch
Patch0568:            0568-seccomp-allow-turning-off-of-seccomp-filtering-via-e.patch
Patch0569:            0569-meson-remove-strange-dep-that-causes-meson-to-enter-.patch
Patch0570:            0570-copy-handle-copy_file_range-weirdness-on-procfs-sysf.patch
Patch0571:            0571-core-Hide-Deactivated-successfully-message.patch
Patch0572:            0572-util-rework-in_initrd-to-make-use-of-path_is_tempora.patch
Patch0573:            0573-initrd-extend-SYSTEMD_IN_INITRD-to-accept-non-ramfs-.patch
Patch0574:            0574-initrd-do-a-debug-log-if-failed-to-detect-rootfs-typ.patch
Patch0575:            0575-initrd-do-a-debug-log-if-etc-initrd-release-doesn-t-.patch
Patch0576:            0576-units-assign-user-runtime-dir-.service-to-user-i.sli.patch
Patch0577:            0577-units-order-user-runtime-dir-.service-after-systemd-.patch
Patch0578:            0578-units-make-sure-user-runtime-dir-.service-is-Type-on.patch
Patch0579:            0579-user-runtime-dir-downgrade-a-few-log-messages-to-LOG.patch
Patch0580:            0580-shared-install-Preserve-escape-characters-for-escape.patch
Patch0581:            0581-basic-virt-Detect-PowerVM-hypervisor.patch
Patch0582:            0582-man-document-differences-in-clean-exit-status-for-Ty.patch
Patch0583:            0583-busctl-add-a-timestamp-to-the-output-of-the-busctl-m.patch
Patch0584:            0584-basic-cap-list-parse-print-numerical-capabilities.patch
Patch0585:            0585-shared-mount-util-convert-to-libmount.patch
Patch0586:            0586-mount-util-bind_remount-avoid-calling-statvfs.patch
Patch0587:            0587-mount-util-use-UMOUNT_NOFOLLOW-in-recursive-umounter.patch
Patch0588:            0588-test-install-root-create-referenced-targets.patch
Patch0589:            0589-install-warn-if-WantedBy-targets-don-t-exist.patch
Patch0590:            0590-test-install-root-add-test-for-unknown-WantedBy-targ.patch
Patch0591:            0591-ceph-is-a-network-filesystem.patch
Patch0592:            0592-sysctl-set-kernel.core_pipe_limit-16.patch
Patch0593:            0593-core-don-t-drop-timer-expired-but-not-yet-processed-.patch
Patch0594:            0594-core-Detect-initial-timer-state-from-serialized-data.patch
Patch0595:            0595-rc-local-order-after-network-online.target.patch
Patch0596:            0596-set-core-ulimit-to-0-like-on-RHEL-7.patch
Patch0597:            0597-test-mountpointutil-util-do-not-assert-in-test_mnt_i.patch
Patch0598:            0598-remove-a-left-over-break.patch
Patch0599:            0599-basic-unit-name-do-not-use-strdupa-on-a-path.patch
Patch0600:            0600-sd-event-change-ordering-of-pending-ratelimited-even.patch
Patch0601:            0601-sd-event-drop-unnecessary-else.patch
Patch0602:            0602-sd-event-use-CMP-macro.patch
Patch0603:            0603-sd-event-use-usec_add.patch
Patch0604:            0604-sd-event-make-event_source_time_prioq_reshuffle-acce.patch
Patch0605:            0605-sd-event-always-reshuffle-time-prioq-on-changing-onl.patch
Patch0606:            0606-ci-run-unit-tests-on-z-stream-branches-as-well.patch
Patch0607:            0607-ci-drop-forgotten-Travis-references.patch
Patch0608:            0608-ci-run-unit-tests-on-CentOS-8-Stream-as-well.patch
Patch0609:            0609-ci-add-missing-test-dependencies.patch
Patch0610:            0610-meson-bump-timeout-for-test-udev-to-180s.patch
Patch0611:            0611-Added-option-check-inhibitors-for-non-tty-usage.patch
Patch0612:            0612-logind-Introduce-RebootWithFlags-and-others.patch
Patch0613:            0613-logind-add-WithFlags-methods-to-policy.patch
Patch0614:            0614-logind-simplify-flags-handling-a-bit.patch
Patch0615:            0615-Update-link-to-RHEL-documentation.patch
Patch0616:            0616-Set-default-core-ulimit-to-0-but-keep-the-hard-limit.patch
Patch0617:            0617-shared-seccomp-util-address-family-filtering-is-brok.patch
Patch0618:            0618-logind-rework-Seat-Session-User-object-allocation-an.patch
Patch0619:            0619-logind-fix-serialization-deserialization-of-user-s-d.patch
Patch0620:            0620-logind-turn-of-stdio-locking-when-writing-session-fi.patch
Patch0621:            0621-units-set-StopWhenUnneeded-for-the-user-slice-units-.patch
Patch0622:            0622-units-improve-Description-string-a-bit.patch
Patch0623:            0623-logind-improve-logging-in-manager_connect_console.patch
Patch0624:            0624-logind-save-restore-User-object-s-stopping-field-dur.patch
Patch0625:            0625-logind-correct-bad-clean-up-path.patch
Patch0626:            0626-logind-fix-bad-error-propagation.patch
Patch0627:            0627-logind-never-elect-a-session-that-is-stopping-as-dis.patch
Patch0628:            0628-logind-introduce-little-helper-that-checks-whether-a.patch
Patch0629:            0629-logind-propagate-session-stop-errors.patch
Patch0630:            0630-logind-rework-how-we-manage-the-slice-and-user-runti.patch
Patch0631:            0631-logind-optionally-keep-the-user-.service-instance-fo.patch
Patch0632:            0632-logind-add-a-RequiresMountsFor-dependency-from-the-s.patch
Patch0633:            0633-logind-improve-error-propagation-of-user_check_linge.patch
Patch0634:            0634-logind-automatically-GC-lingering-users-for-who-now-.patch
Patch0635:            0635-pam_systemd-simplify-code-which-with-we-set-environm.patch
Patch0636:            0636-logind-validate-run-user-1000-before-we-set-it.patch
Patch0637:            0637-sd-hwdb-allow-empty-properties.patch
Patch0638:            0638-Update-hwdb.patch
Patch0639:            0639-Disable-libpitc-to-fix-CentOS-Stream-CI.patch
Patch0640:            0640-rpm-Fix-typo-in-_environmentdir.patch
Patch0641:            0641-rpm-Add-misspelled-_environmentdir-macro-for-tempora.patch
Patch0642:            0642-rpm-emit-warning-when-macro-with-typo-is-used.patch
Patch0643:            0643-Remove-unintended-additions-to-systemd-analyze-man-p.patch
Patch0644:            0644-Disable-iptables-for-CI.patch
Patch0645:            0645-core-fix-SIGABRT-on-empty-exec-command-argv.patch
Patch0646:            0646-core-service-also-check-path-in-exec-commands.patch
Patch0647:            0647-mount-util-fix-fd_is_mount_point-when-both-the-paren.patch
Patch0648:            0648-basic-add-vmware-hypervisor-detection-from-device-tr.patch
Patch0649:            0649-pam-do-not-require-a-non-expired-password-for-user-..patch
Patch0650:            0650-udev-rules-add-rule-to-create-dev-ptp_hyperv.patch
Patch0651:            0651-process-util-explicitly-handle-processes-lacking-par.patch
Patch0652:            0652-errno-util-add-ERRNO_IS_PRIVILEGE-helper.patch
Patch0653:            0653-procfs-util-fix-confusion-wrt.-quantity-limit-and-ma.patch
Patch0654:            0654-test-process-util-also-add-EROFS-to-the-list-of-good.patch
Patch0655:            0655-journal-refresh-cached-credentials-of-stdout-streams.patch
Patch0656:            0656-util-lib-introduce-HAS_FEATURE_ADDRESS_SANITIZER.patch
Patch0657:            0657-ci-skip-test-execute-on-GH-Actions-under-ASan.patch
Patch0658:            0658-test-seccomp-accept-ENOSYS-from-sysctl-2-too.patch
Patch0659:            0659-test-accept-that-char-device-0-0-can-now-be-created-.patch
Patch0660:            0660-meson-do-not-fail-if-rsync-is-not-installed-with-mes.patch
Patch0661:            0661-pid1-fix-free-of-uninitialized-pointer-in-unit_fail_.patch
Patch0662:            0662-sd-event-take-ref-on-event-loop-object-before-dispat.patch
Patch0663:            0663-core-consider-service-with-no-start-command-immediat.patch
Patch0664:            0664-man-move-description-of-Action-modes-to-FailureActio.patch
Patch0665:            0665-core-define-exit-and-exit-force-actions-for-user-uni.patch
Patch0666:            0666-core-accept-system-mode-emergency-action-specifiers-.patch
Patch0667:            0667-core-allow-services-with-no-commands-but-SuccessActi.patch
Patch0668:            0668-core-limit-service-watchdogs-no-to-actual-watchdog-c.patch
Patch0669:            0669-units-use-SuccessAction-exit-force-in-systemd-exit.s.patch
Patch0670:            0670-units-use-SuccessAction-reboot-force-in-systemd-rebo.patch
Patch0671:            0671-units-use-SuccessAction-poweroff-force-in-systemd-po.patch
Patch0672:            0672-units-allow-and-use-SuccessAction-exit-force-in-syst.patch
Patch0673:            0673-core-do-not-warn-about-mundane-emergency-actions.patch
Patch0674:            0674-core-return-true-from-cg_is_empty-on-ENOENT.patch
Patch0675:            0675-macro-define-HAS_FEATURE_ADDRESS_SANITIZER-also-on-g.patch
Patch0676:            0676-tests-add-helper-function-to-autodetect-CI-environme.patch
Patch0677:            0677-strv-rework-FOREACH_STRING-macro.patch
Patch0678:            0678-test-systemctl-use-const-char-instead-of-char.patch
Patch0679:            0679-ci-pass-the-GITHUB_ACTIONS-variable-to-the-CentOS-co.patch
Patch0680:            0680-lgtm-detect-uninitialized-variables-using-the-__clea.patch
Patch0681:            0681-lgtm-replace-the-query-used-for-looking-for-fgets-wi.patch
Patch0682:            0682-lgtm-beef-up-list-of-dangerous-questionnable-API-cal.patch
Patch0683:            0683-lgtm-warn-about-strerror-use.patch
Patch0684:            0684-lgtm-complain-about-accept-people-should-use-accept4.patch
Patch0685:            0685-lgtm-don-t-treat-the-custom-note-as-a-list-of-tags.patch
Patch0686:            0686-lgtm-ignore-certain-cleanup-functions.patch
Patch0687:            0687-lgtm-detect-more-possible-problematic-scenarios.patch
Patch0688:            0688-lgtm-enable-more-and-potentially-useful-queries.patch
Patch0689:            0689-meson-avoid-bogus-meson-warning.patch
Patch0690:            0690-test-make-TEST-47-less-racy.patch
Patch0691:            0691-core-rename-unit_-start_limit-condition-assert-_test.patch
Patch0692:            0692-core-Check-unit-start-rate-limiting-earlier.patch
Patch0693:            0693-sd-event-introduce-callback-invoked-when-event-sourc.patch
Patch0694:            0694-core-rename-generalize-UNIT-u-test_start_limit-hook.patch
Patch0695:            0695-mount-make-mount-units-start-jobs-not-runnable-if-p-.patch
Patch0696:            0696-mount-retrigger-run-queue-after-ratelimit-expired-to.patch
Patch0697:            0697-pid1-add-a-manager_trigger_run_queue-helper.patch
Patch0698:            0698-unit-add-jobs-that-were-skipped-because-of-ratelimit.patch
Patch0699:            0699-Revert-Revert-sysctl-Enable-ping-8-inside-rootless-P.patch
Patch0700:            0700-sysctl-prefix-ping-port-range-setting-with-a-dash.patch
Patch0701:            0701-mount-don-t-propagate-errors-from-mount_setup_unit-f.patch
Patch0702:            0702-udev-net_id-introduce-naming-scheme-for-RHEL-8.5.patch
Patch0703:            0703-udev-net_id-remove-extraneous-bracket.patch
Patch0704:            0704-udev-net_id-introduce-naming-scheme-for-RHEL-8.6.patch
Patch0705:            0705-define-newly-needed-constants.patch
Patch0706:            0706-sd-netlink-support-IFLA_PROP_LIST-and-IFLA_ALT_IFNAM.patch
Patch0707:            0707-sd-netlink-introduce-sd_netlink_message_read_strv.patch
Patch0708:            0708-sd-netlink-introduce-sd_netlink_message_append_strv.patch
Patch0709:            0709-test-add-a-test-for-sd_netlink_message_-append-read-.patch
Patch0710:            0710-util-introduce-ifname_valid_full.patch
Patch0711:            0711-rename-function.patch
Patch0712:            0712-udev-support-AlternativeName-setting-in-.link-file.patch
Patch0713:            0713-network-make-Name-in-Match-support-alternative-names.patch
Patch0714:            0714-udev-extend-the-length-of-ID_NET_NAME_XXX-to-ALTIFNA.patch
Patch0715:            0715-udev-do-not-fail-if-kernel-does-not-support-alternat.patch
Patch0716:            0716-udev-introduce-AlternativeNamesPolicy-setting.patch
Patch0717:            0717-network-set-AlternativeNamesPolicy-in-99-default.lin.patch
Patch0718:            0718-random-util-call-initialize_srand-after-fork.patch
Patch0719:            0719-sd-netlink-introduce-rtnl_resolve_link_alternative_n.patch
Patch0720:            0720-udev-sort-alternative-names.patch
Patch0721:            0721-netlink-introduce-rtnl_get-delete_link_alternative_n.patch
Patch0722:            0722-netlink-do-not-fail-when-new-interface-name-is-alrea.patch
Patch0723:            0723-udev-do-not-try-to-reassign-alternative-names.patch
Patch0724:            0724-Do-not-fail-if-the-same-alt.-name-is-set-again.patch
Patch0725:            0725-mount-do-not-update-exec-deps-on-mountinfo-changes.patch
Patch0726:            0726-core-mount-add-implicit-unit-dependencies-even-if-wh.patch
Patch0727:            0727-core-fix-unfortunate-typo-in-unit_is_unneeded.patch
Patch0728:            0728-core-make-destructive-transaction-error-a-bit-more-u.patch
Patch0729:            0729-tmpfiles-use-a-entry-in-hashmap-as-ItemArray-in-read.patch
Patch0730:            0730-tmpfiles-rework-condition-check.patch
Patch0731:            0731-TEST-22-TMPFILES-add-reproducer-for-bug-with-X.patch
Patch0732:            0732-core-make-sure-we-don-t-get-confused-when-setting-TE.patch
Patch0733:            0733-hash-funcs-introduce-macro-to-create-typesafe-hash_o.patch
Patch0734:            0734-hash-func-add-destructors-for-key-and-value.patch
Patch0735:            0735-util-define-free_func_t.patch
Patch0736:            0736-hash-funcs-make-basic-hash_ops-typesafe.patch
Patch0737:            0737-test-add-tests-for-destructors-of-hashmap-or-set.patch
Patch0738:            0738-man-document-the-new-sysctl.d-prefix.patch
Patch0739:            0739-sysctl-if-options-are-prefixed-with-ignore-write-err.patch
Patch0740:            0740-sysctl-fix-segfault.patch
Patch0741:            0741-ci-drop-CentOS-8-CI.patch
Patch0742:            0742-test-adapt-to-the-new-capsh-format.patch
Patch0743:            0743-test-ignore-IAB-capabilities-in-test-execute.patch
Patch0744:            0744-core-disallow-using-.service-as-a-service-name.patch
Patch0745:            0745-shared-dropin-support-.service.d-top-level-drop-in-f.patch
Patch0746:            0746-core-change-top-level-drop-in-from-.service.d-to-ser.patch
Patch0747:            0747-shared-dropin-fix-assert-for-invalid-drop-in.patch
Patch0748:            0748-udev-fix-slot-based-network-names-on-s390.patch
Patch0749:            0749-udev-add-missing-initialization-to-fix-freeing-inval.patch
Patch0750:            0750-udev-it-is-not-necessary-that-the-path-is-readable.patch
Patch0751:            0751-udev-allow-onboard-index-up-to-65535.patch
Patch0752:            0752-Revert-basic-use-comma-as-separator-in-cpuset-cgroup.patch
Patch0753:            0753-acpi-fpdt-mark-structures-as-packed.patch
Patch0754:            0754-core-slice-make-slice_freezer_action-return-0-if-fre.patch
Patch0755:            0755-core-unit-fix-use-after-free.patch
Patch0756:            0756-sd-bus-fix-reference-counter-to-be-incremented.patch
Patch0757:            0757-sd-bus-do-not-read-unused-value.patch
Patch0758:            0758-sd-bus-do-not-return-negative-errno-when-unknown-nam.patch
Patch0759:            0759-sd-bus-switch-to-a-manual-overflow-check-in-sd_bus_t.patch
Patch0760:            0760-resolved-let-s-preferably-route-reverse-lookups-for-.patch
Patch0761:            0761-unit-don-t-emit-PropertiesChanged-signal-if-adding-a.patch
Patch0762:            0762-tests-make-inverted-tests-actually-count.patch
Patch0763:            0763-TEST-make-failure-tests-actually-fail-on-failure.patch
Patch0764:            0764-ci-Mergify-configuration-update.patch
Patch0765:            0765-core-propagate-triggered-unit-in-more-load-states.patch
Patch0766:            0766-core-propagate-unit-start-limit-hit-state-to-trigger.patch
Patch0767:            0767-core-Move-r-variable-declaration-to-start-of-unit_st.patch
Patch0768:            0768-core-Delay-start-rate-limit-check-when-starting-a-un.patch
Patch0769:            0769-core-Propagate-condition-failed-state-to-triggering-.patch
Patch0770:            0770-unit-check-for-mount-rate-limiting-before-checking-a.patch
Patch0771:            0771-mkosi-Add-gnutls-package.patch
Patch0772:            0772-unit-name-tighten-checks-for-building-valid-unit-nam.patch
Patch0773:            0773-core-shorten-long-unit-names-that-are-based-on-paths.patch
Patch0774:            0774-test-add-extended-test-for-triggering-mount-rate-lim.patch
Patch0775:            0775-tests-add-test-case-for-long-unit-names.patch
Patch0776:            0776-core-unset-HOME-that-the-kernel-gives-us.patch
Patch0777:            0777-journal-remote-check-return-value-from-MHD_add_respo.patch
Patch0778:            0778-journalctl-in-follow-mode-watch-stdout-for-POLLHUP-P.patch
Patch0779:            0779-sd-bus-make-BUS_DEFAULT_TIMEOUT-configurable.patch
Patch0780:            0780-fstab-generator-fix-debug-log.patch
Patch0781:            0781-logind-session-dbus-allow-to-set-display-name-via-db.patch
Patch0782:            0782-Allow-restart-for-oneshot-units.patch
Patch0783:            0783-test-correct-TEST-41-StartLimitBurst-test.patch
Patch0784:            0784-core-fix-assert-about-number-of-built-environment-va.patch
Patch0785:            0785-core-add-one-more-assert.patch
Patch0786:            0786-strv-introduce-strv_join_prefix.patch
Patch0787:            0787-test-add-tests-for-strv_join_prefix.patch
Patch0788:            0788-test-replace-swear-words-by-hoge.patch
Patch0789:            0789-core-add-new-environment-variable-RUNTIME_DIRECTORY-.patch
Patch0790:            0790-test-execute-add-tests-for-RUNTIME_DIRECTORY-or-frie.patch
Patch0791:            0791-man-document-RUNTIME_DIRECTORY-or-friends.patch
Patch0792:            0792-ci-bump-the-worker-Ubuntu-version-to-Jammy.patch
Patch0793:            0793-test-make-test-execute-pass-on-Linux-5.15.patch
Patch0794:            0794-ci-install-iputils.patch
Patch0795:            0795-ci-Mergify-Add-ci-waived-logic.patch
Patch0796:            0796-sd-event-don-t-invalidate-source-type-on-disconnect.patch
Patch0797:            0797-tests-make-sure-we-delay-running-mount-start-jobs-wh.patch
Patch0798:            0798-core-drop-references-to-StandardOutputFileToCreate.patch
Patch0799:            0799-dbus-execute-fix-indentation.patch
Patch0800:            0800-dbus-execute-generate-the-correct-transient-unit-set.patch
Patch0801:            0801-bus-unit-util-properly-accept-StandardOutput-append-.patch
Patch0802:            0802-core-be-more-careful-when-inheriting-stdout-fds-to-s.patch
Patch0803:            0803-test-add-a-test-for-StandardError-file.patch
Patch0804:            0804-tree-wide-allow-ASCII-fallback-for-in-logs.patch
Patch0805:            0805-tree-wide-allow-ASCII-fallback-for-in-logs.patch
Patch0806:            0806-core-allow-to-set-default-timeout-for-devices.patch
Patch0807:            0807-man-document-DefaultDeviceTimeoutSec.patch
Patch0808:            0808-Revert-core-Propagate-condition-failed-state-to-trig.patch
Patch0809:            0809-core-Check-unit-start-rate-limiting-earlier.patch
Patch0810:            0810-core-Add-trigger-limit-for-path-units.patch
Patch0811:            0811-meson-add-syscall-names-update-target.patch
Patch0812:            0812-syscall-names-add-process_madvise-which-is-planned-f.patch
Patch0813:            0813-shared-add-known-syscall-list.patch
Patch0814:            0814-generate-syscall-list-require-python3.patch
Patch0815:            0815-shared-seccomp-reduce-scope-of-indexing-variables.patch
Patch0816:            0816-shared-syscall-list-filter-out-some-obviously-platfo.patch
Patch0817:            0817-seccomp-tighten-checking-of-seccomp-filter-creation.patch
Patch0818:            0818-shared-seccomp-util-added-functionality-to-make-list.patch
Patch0819:            0819-nspawn-return-ENOSYS-by-default-EPERM-for-known-call.patch
Patch0820:            0820-test-procfs-util-skip-test-on-certain-errors.patch
Patch0821:            0821-Try-stopping-MD-RAID-devices-in-shutdown-too.patch
Patch0822:            0822-shutdown-get-only-active-md-arrays.patch
Patch0823:            0823-scope-allow-unprivileged-delegation-on-scopes.patch
Patch0824:            0824-resolved-pin-stream-while-calling-callbacks-for-it.patch
Patch0825:            0825-ci-functions-Add-useradd-and-userdel.patch
Patch0826:            0826-logind-optionally-watch-utmp-for-login-data.patch
Patch0827:            0827-logind-add-hashtable-for-finding-session-by-leader-P.patch
Patch0828:            0828-core-load-fragment-move-config_parse_sec_fix_0-to-sr.patch
Patch0829:            0829-sd-event-add-relative-timer-calls.patch
Patch0830:            0830-logind-add-option-to-stop-idle-sessions-after-specif.patch
Patch0831:            0831-logind-schedule-idle-check-full-interval-from-now-if.patch
Patch0832:            0832-ci-lint-add-shell-linter-Differential-ShellCheck.patch
Patch0833:            0833-meson-do-not-compare-objects-of-different-types.patch
Patch0834:            0834-journal-remote-use-MHD_HTTP_CONTENT_TOO_LARGE-as-MHD.patch
Patch0835:            0835-Fix-build-with-httpd-0.9.71.patch
Patch0836:            0836-ci-replace-LGTM-with-CodeQL.patch
Patch0837:            0837-ci-mergify-Update-policy-Drop-LGTM-checks.patch
Patch0838:            0838-time-util-fix-buffer-over-run.patch
Patch0839:            0839-basic-recognize-pdfs-filesystem-as-a-network-filesys.patch
Patch0840:            0840-core-move-reset_arguments-to-the-end-of-main-s-finis.patch
Patch0841:            0841-manager-move-inc.-of-n_reloading-into-a-function.patch
Patch0842:            0842-core-Add-new-DBUS-properties-UnitsReloadStartTimesta.patch
Patch0843:            0843-core-Indicate-the-time-when-the-manager-started-load.patch
Patch0844:            0844-core-do-not-touch-run-systemd-systemd-units-load-fro.patch
Patch0845:            0845-sysctl-downgrade-message-when-we-have-no-permission.patch
Patch0846:            0846-core-respect-SELinuxContext-for-socket-creation.patch
Patch0847:            0847-manager-use-target-process-context-to-set-socket-con.patch
Patch0848:            0848-virt-detect-Amazon-EC2-Nitro-instance.patch
Patch0849:            0849-machine-id-setup-generate-machine-id-from-DMI-produc.patch
Patch0850:            0850-virt-use-string-table-to-detect-VM-or-container.patch
Patch0851:            0851-fileio-introduce-read_full_virtual_file-for-reading-.patch
Patch0852:            0852-Use-BIOS-characteristics-to-distinguish-EC2-bare-met.patch
Patch0853:            0853-device-drop-refuse_after.patch
Patch0854:            0854-manager-limit-access-to-private-dbus-socket.patch
Patch0855:            0855-journalctl-do-not-treat-EINTR-as-an-error-when-waiti.patch
Patch0856:            0856-core-bring-manager_startup-and-manager_reload-more-i.patch
Patch0857:            0857-pam-add-a-call-to-pam_namespace.patch
Patch0858:            0858-virt-Support-detection-for-ARM64-Hyper-V-guests.patch
Patch0859:            0859-virt-Fix-the-detection-for-Hyper-V-VMs.patch
Patch0860:            0860-basic-add-STRERROR-wrapper-for-strerror_r.patch
Patch0861:            0861-coredump-put-context-array-into-a-struct.patch
Patch0862:            0862-coredump-do-not-allow-user-to-access-coredumps-with-.patch
Patch0863:            0863-logind-remember-our-idle-state-and-use-it-to-detect-.patch
Patch0864:            0864-test-import-logind-test-from-debian-ubuntu-test-suit.patch
Patch0865:            0865-test-introduce-inst_recursive-helper-function.patch
Patch0866:            0866-tests-verify-that-Lock-D-Bus-signal-is-sent-when-Idl.patch
Patch0867:            0867-systemctl-simplify-halt_main.patch
Patch0868:            0868-systemctl-shutdown-don-t-fallback-on-auth-fail.patch
Patch0869:            0869-systemctl-reintroduce-the-original-halt_main.patch
Patch0870:            0870-systemctl-preserve-old-behavior-unless-requested.patch
Patch0871:            0871-pam_systemd-suppress-LOG_DEBUG-log-messages-if-debug.patch
Patch0872:            0872-udev-net_id-introduce-naming-scheme-for-RHEL-8.8.patch
Patch0873:            0873-journald-add-API-to-move-logging-from-var-to-run-aga.patch
Patch0874:            0874-journalctl-add-new-relinquish-and-smart-relinquish-o.patch
Patch0875:            0875-units-automatically-revert-to-run-logging-on-shutdow.patch
Patch0876:            0876-pstore-Tool-to-archive-contents-of-pstore.patch
Patch0877:            0877-meson-drop-redundant-line.patch
Patch0878:            0878-pstore-drop-unnecessary-initializations.patch
Patch0879:            0879-pstopre-fix-return-value-of-list_files.patch
Patch0880:            0880-pstore-remove-temporary-file-on-failure.patch
Patch0881:            0881-pstore-do-not-add-FILE-journal-entry-if-content_size.patch
Patch0882:            0882-pstore-run-only-when-sys-fs-pstore-is-not-empty.patch
Patch0883:            0883-pstore-fix-use-after-free.patch
Patch0884:            0884-pstore-refuse-to-run-if-arguments-are-specified.patch
Patch0885:            0885-pstore-allow-specifying-src-and-dst-dirs-are-argumen.patch
Patch0886:            0886-pstore-rework-memory-handling-for-dmesg.patch
Patch0887:            0887-pstore-fixes-for-dmesg.txt-reconstruction.patch
Patch0888:            0888-pstore-Don-t-start-systemd-pstore.service-in-contain.patch
Patch0889:            0889-units-pull-in-systemd-pstore.service-from-sysinit.ta.patch
Patch0890:            0890-units-drop-dependency-on-systemd-remount-fs.service-.patch
Patch0891:            0891-units-make-sure-systemd-pstore-stops-at-shutdown.patch
Patch0892:            0892-pstore-Run-after-modules-are-loaded.patch
Patch0893:            0893-pstore-do-not-try-to-load-all-known-pstore-modules.patch
Patch0894:            0894-logind-session-make-stopping-of-idle-session-visible.patch
Patch0895:            0895-journald-Increase-stdout-buffer-size-sooner-when-alm.patch
Patch0896:            0896-journald-rework-end-of-line-marker-handling-to-use-a.patch
Patch0897:            0897-journald-use-the-fact-that-client_context_release-re.patch
Patch0898:            0898-journald-rework-pid-change-handling.patch
Patch0899:            0899-test-Add-a-test-case-for-15654.patch
Patch0900:            0900-test-Stricter-test-case-for-15654-Add-more-checks.patch
Patch0901:            0901-man-document-the-new-_LINE_BREAK-type.patch
Patch0902:            0902-journald-server-always-create-state-file-in-signal-h.patch
Patch0903:            0903-journald-server-move-relinquish-code-into-function.patch
Patch0904:            0904-journald-server-always-touch-state-file-in-signal-ha.patch
Patch0905:            0905-pager-set-LESSSECURE-whenver-we-invoke-a-pager.patch
Patch0906:            0906-test-login-always-test-sd_pid_get_owner_uid-moderniz.patch
Patch0907:            0907-pager-make-pager-secure-when-under-euid-is-changed-o.patch
Patch0908:            0908-test-ignore-ENOMEDIUM-error-from-sd_pid_get_cgroup.patch
Patch0909:            0909-pstore-fix-crash-and-forward-dummy-arguments-instead.patch
Patch0910:            0910-ci-workflow-for-gathering-metadata-for-source-git-au.patch
Patch0911:            0911-ci-first-part-of-the-source-git-automation-commit-li.patch

%ifarch %{ix86} x86_64 aarch64
%global have_gnu_efi 1
%endif

BuildRequires:        gcc
BuildRequires:        gcc-c++
BuildRequires:        libcap-devel
BuildRequires:        libmount-devel
BuildRequires:        pam-devel
BuildRequires:        libselinux-devel
BuildRequires:        audit-libs-devel
BuildRequires:        cryptsetup-devel
BuildRequires:        dbus-devel
BuildRequires:        libacl-devel
BuildRequires:        gobject-introspection-devel
BuildRequires:        libblkid-devel
BuildRequires:        xz-devel
BuildRequires:        xz
BuildRequires:        lz4-devel
BuildRequires:        lz4
BuildRequires:        bzip2-devel
BuildRequires:        libidn2-devel
BuildRequires:        libcurl-devel
BuildRequires:        kmod-devel
BuildRequires:        elfutils-devel
BuildRequires:        libgcrypt-devel
BuildRequires:        libgpg-error-devel
BuildRequires:        gnutls-devel
BuildRequires:        libmicrohttpd-devel
BuildRequires:        libxkbcommon-devel
BuildRequires:        libxslt
BuildRequires:        docbook-style-xsl
BuildRequires:        pkgconfig
BuildRequires:        gperf
BuildRequires:        gawk
BuildRequires:        tree
BuildRequires:        python3-devel
BuildRequires:        python3-lxml
BuildRequires:        firewalld-filesystem
%if 0%{?have_gnu_efi}
BuildRequires:        gnu-efi gnu-efi-devel
%endif
BuildRequires:        libseccomp-devel
BuildRequires:        git
BuildRequires:        meson >= 0.43
BuildRequires:        gettext

Requires(post): coreutils
Requires(post): sed
Requires(post): acl
Requires(post): grep
# systemd-machine-id-setup requires libssl
Requires(post): openssl-libs
Requires(pre):  coreutils
Requires(pre):  /usr/bin/getent
Requires(pre):  /usr/sbin/groupadd
Requires:             dbus >= 1.9.18
Requires:             %{name}-pam = %{version}-%{release}
Requires:             %{name}-libs = %{version}-%{release}
Recommends:           diffutils
Requires:             util-linux
Recommends:           libxkbcommon%{?_isa}
Provides:             /bin/systemctl
Provides:             /sbin/shutdown
Provides:             syslog
Provides:             systemd-units = %{version}-%{release}
Provides:             systemd-rpm-macros = %{version}-%{release}
Obsoletes:            system-setup-keyboard < 0.9
Provides:             system-setup-keyboard = 0.9
# systemd-sysv-convert was removed in f20: https://fedorahosted.org/fpc/ticket/308
Obsoletes:            systemd-sysv < 206
# self-obsoletes so that dnf will install new subpackages on upgrade (#1260394)
Obsoletes:            %{name} < 229-5
Provides:             systemd-sysv = 206
Conflicts:            initscripts < 9.56.1
%if 0%{?fedora}
Conflicts:            fedora-release < 23-0.12
%endif

%description
systemd is a system and service manager that runs as PID 1 and starts
the rest of the system. It provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux control groups, maintains mount and automount points, and
implements an elaborate transactional dependency-based service control
logic. systemd supports SysV and LSB init scripts and works as a
replacement for sysvinit. Other parts of this package are a logging daemon,
utilities to control basic system configuration like the hostname,
date, locale, maintain a list of logged-in users, system accounts,
runtime directories and settings, and daemons to manage simple network
configuration, network time synchronization, log forwarding, and name
resolution.

%package libs
Summary:              systemd libraries
License:              LGPLv2+ and MIT
Obsoletes:            libudev < 183
Obsoletes:            systemd < 185-4
Conflicts:            systemd < 185-4
Obsoletes:            systemd-compat-libs < 230
Obsoletes:            nss-myhostname < 0.4
Provides:             nss-myhostname = 0.4
Provides:             nss-myhostname%{_isa} = 0.4
Requires(post): coreutils
Requires(post): sed
Requires(post): grep
Requires(post): /usr/bin/getent

%description libs
Libraries for systemd and udev.

%package pam
Summary:              systemd PAM module
Requires:             %{name} = %{version}-%{release}

%description pam
Systemd PAM module registers the session with systemd-logind.

%package devel
Summary:              Development headers for systemd
License:              LGPLv2+ and MIT
Requires:             %{name}-libs%{?_isa} = %{version}-%{release}
Provides:             libudev-devel = %{version}
Provides:             libudev-devel%{_isa} = %{version}
Obsoletes:            libudev-devel < 183
# Fake dependency to make sure systemd-pam is pulled into multilib (#1414153)
Requires:             %{name}-pam = %{version}-%{release}

%description devel
Development headers and auxiliary files for developing applications linking
to libudev or libsystemd.

%package udev
Summary:              Rule-based device node and kernel event manager
Requires:             %{name}%{?_isa} = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(post): grep
Requires:             kmod >= 18-4
# obsolete parent package so that dnf will install new subpackage on upgrade (#1260394)
Obsoletes:            %{name} < 229-5
Provides:             udev = %{version}
Provides:             udev%{_isa} = %{version}
Obsoletes:            udev < 183
# https://bugzilla.redhat.com/show_bug.cgi?id=1408878
Recommends:           kbd
License:              LGPLv2+

%description udev
This package contains systemd-udev and the rules and hardware database
needed to manage device nodes. This package is necessary on physical
machines and in virtual machines, but not in containers.

%package container
# Name is the same as in Debian
Summary:              Tools for containers and VMs
Requires:             %{name}%{?_isa} = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
# obsolete parent package so that dnf will install new subpackage on upgrade (#1260394)
Obsoletes:            %{name} < 229-5
License:              LGPLv2+

%description container
Systemd tools to spawn and manage containers and virtual machines.

This package contains systemd-nspawn, machinectl, systemd-machined,
and systemd-importd.

%package journal-remote
# Name is the same as in Debian
Summary:              Tools to send journal events over the network
Requires:             %{name}%{?_isa} = %{version}-%{release}
License:              LGPLv2+
Requires(pre):    /usr/bin/getent
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires:             firewalld-filesystem
Provides:             %{name}-journal-gateway = %{version}-%{release}
Provides:             %{name}-journal-gateway%{_isa} = %{version}-%{release}
Obsoletes:            %{name}-journal-gateway < 227-7

%description journal-remote
Programs to forward journal entries over the network, using encrypted HTTP,
and to write journal files from serialized journal contents.

This package contains systemd-journal-gatewayd,
systemd-journal-remote, and systemd-journal-upload.

%package tests
Summary:              Internal unit tests for systemd
Requires:             %{name}%{?_isa} = %{version}-%{release}
License:              LGPLv2+

%description tests
"Installed tests" that are usually run as part of the build system.
They can be useful to test systemd internals.

%prep
%autosetup %{?gitcommit:-n %{name}-%{gitcommit}} -S git_am

%build
%define ntpvendor %(source /etc/os-release; echo ${ID})
%{!?ntpvendor: echo 'NTP vendor zone is not set!'; exit 1}

CONFIGURE_OPTS=(
        -Dsysvinit-path=/etc/rc.d/init.d
        -Drc-local=/etc/rc.d/rc.local
        -Dntp-servers='0.%{ntpvendor}.pool.ntp.org 1.%{ntpvendor}.pool.ntp.org 2.%{ntpvendor}.pool.ntp.org 3.%{ntpvendor}.pool.ntp.org'
        -Ddns-servers=''
        -Ddev-kvm-mode=0666
        -Dkmod=true
        -Dxkbcommon=true
        -Dblkid=true
        -Dseccomp=true
        -Dima=true
        -Dselinux=true
        -Dapparmor=false
        -Dpolkit=true
        -Dxz=true
        -Dzlib=true
        -Dbzip2=true
        -Dlz4=true
        -Dpam=true
        -Dacl=true
        -Dsmack=true
        -Dgcrypt=true
        -Daudit=true
        -Delfutils=true
        -Dlibcryptsetup=true
        -Delfutils=true
        -Dqrencode=false
        -Dgnutls=true
        -Dmicrohttpd=true
        -Dlibidn2=true
        -Dlibiptc=false
        -Dlibcurl=true
        -Defi=true
        -Dgnu-efi=%{?have_gnu_efi:true}%{?!have_gnu_efi:false}
        -Dtpm=true
        -Dhwdb=true
        -Dsysusers=true
        -Ddefault-kill-user-processes=false
        -Dtests=unsafe
        -Dinstall-tests=true
        -Dtty-gid=5
        -Dusers-gid=100
        -Dnobody-user=nobody
        -Dnobody-group=nobody
        -Dsplit-usr=false
        -Dsplit-bin=true
        -Db_lto=false
        -Dnetworkd=false
        -Dtimesyncd=false
        -Ddefault-hierarchy=legacy
        -Dversion-tag=%{version}-%{release}
)

# Don't ship /var/log/README. The relationship between journal and syslog should be documented
# in the official documentation.
sed -ie "/subdir('doc\/var-log')/d" meson.build

%meson "${CONFIGURE_OPTS[@]}"
%meson_build

if diff %{SOURCE1} %{_vpath_builddir}/triggers.systemd; then
   echo -e "\n\n\nWARNING: triggers.systemd in Source1 is different!"
   echo -e "      cp %{_vpath_builddir}/triggers.systemd %{SOURCE1}\n\n\n"
fi

%install
%meson_install

# udev links
mkdir -p %{buildroot}/%{_sbindir}
ln -sf ../bin/udevadm %{buildroot}%{_sbindir}/udevadm

# Compatiblity and documentation files
touch %{buildroot}/etc/crypttab
chmod 600 %{buildroot}/etc/crypttab

# /etc/initab
install -Dm0644 -t %{buildroot}/etc/ %{SOURCE5}

# /etc/sysctl.conf compat
install -Dm0644 %{SOURCE6} %{buildroot}/etc/sysctl.conf
ln -s ../sysctl.conf %{buildroot}/etc/sysctl.d/99-sysctl.conf

# We create all wants links manually at installation time to make sure
# they are not owned and hence overriden by rpm after the user deleted
# them.
rm -r %{buildroot}%{_sysconfdir}/systemd/system/*.target.wants

# Make sure these directories are properly owned
mkdir -p %{buildroot}%{system_unit_dir}/basic.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/default.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/dbus.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/syslog.target.wants
mkdir -p %{buildroot}%{_localstatedir}/run
mkdir -p %{buildroot}%{_localstatedir}/log
touch %{buildroot}%{_localstatedir}/log/lastlog
chmod 0664 %{buildroot}%{_localstatedir}/log/lastlog
touch %{buildroot}%{_localstatedir}/run/utmp
touch %{buildroot}%{_localstatedir}/log/{w,b}tmp

# Make sure the user generators dir exists too
mkdir -p %{buildroot}%{pkgdir}/system-generators
mkdir -p %{buildroot}%{pkgdir}/user-generators

# Create new-style configuration files so that we can ghost-own them
touch %{buildroot}%{_sysconfdir}/hostname
touch %{buildroot}%{_sysconfdir}/vconsole.conf
touch %{buildroot}%{_sysconfdir}/locale.conf
touch %{buildroot}%{_sysconfdir}/machine-id
touch %{buildroot}%{_sysconfdir}/machine-info
touch %{buildroot}%{_sysconfdir}/localtime
mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d
touch %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf

# Make sure the shutdown/sleep drop-in dirs exist
mkdir -p %{buildroot}%{pkgdir}/system-shutdown/
mkdir -p %{buildroot}%{pkgdir}/system-sleep/

# Make sure directories in /var exist
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/coredump
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/catalog
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/backlight
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/rfkill
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/linger
mkdir -p %{buildroot}%{_localstatedir}/lib/private
mkdir -p %{buildroot}%{_localstatedir}/log/private
mkdir -p %{buildroot}%{_localstatedir}/cache/private
mkdir -p %{buildroot}%{_localstatedir}/lib/private/systemd/journal-upload
ln -s ../private/systemd/journal-upload %{buildroot}%{_localstatedir}/lib/systemd/journal-upload
mkdir -p %{buildroot}%{_localstatedir}/log/journal
touch %{buildroot}%{_localstatedir}/lib/systemd/catalog/database
touch %{buildroot}%{_sysconfdir}/udev/hwdb.bin
touch %{buildroot}%{_localstatedir}/lib/systemd/random-seed
touch %{buildroot}%{_localstatedir}/lib/private/systemd/journal-upload/state

# Install rc.local
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/
install -m 0644 %{SOURCE13} %{buildroot}%{_sysconfdir}/rc.d/rc.local
ln -s rc.d/rc.local %{buildroot}%{_sysconfdir}/rc.local

# Install yum protection fragment
install -Dm0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/dnf/protected.d/systemd.conf

install -Dm0644 -t %{buildroot}/usr/lib/firewalld/services/ %{SOURCE7} %{SOURCE8}

# Restore systemd-user pam config from before "removal of Fedora-specific bits"
install -Dm0644 -t %{buildroot}/etc/pam.d/ %{SOURCE12}

# Install additional docs
# https://bugzilla.redhat.com/show_bug.cgi?id=1234951
install -Dm0644 -t %{buildroot}%{_pkgdocdir}/ %{SOURCE9}

# https://bugzilla.redhat.com/show_bug.cgi?id=1378974
install -Dm0644 -t %{buildroot}%{system_unit_dir}/systemd-udev-trigger.service.d/ %{SOURCE10}

install -Dm0755 -t %{buildroot}%{_prefix}/lib/kernel/install.d/ %{SOURCE11}

install -D -t %{buildroot}/usr/lib/systemd/ %{SOURCE3}

# No tmp-on-tmpfs by default in RHEL. bz#876122 bz#1578772
rm -f %{buildroot}%{_prefix}/lib/systemd/system/local-fs.target.wants/tmp.mount

# bz#1844465
rm -f %{buildroot}/etc/systemd/system/dbus-org.freedesktop.resolve1.service

%find_lang %{name}

# Split files in build root into rpms. See split-files.py for the
# rules towards the end, anything which is an exception needs a line
# here.
python3 %{SOURCE2} %buildroot <<EOF
%ghost %config(noreplace) /etc/crypttab
%ghost %verify (not mode) /etc/udev/hwdb.bin
/etc/inittab
/etc/yum/protected.d/systemd.conf
/usr/lib/systemd/purge-nobody-user
%ghost %config(noreplace) /etc/vconsole.conf
%ghost %config(noreplace) /etc/X11/xorg.conf.d/00-keyboard.conf
%ghost %attr(0664,root,utmp) /var/run/utmp
%ghost %attr(0664,root,utmp) /var/log/wtmp
%ghost %attr(0660,root,utmp) /var/log/btmp
%ghost %attr(0664,root,utmp) %verify(not md5 size mtime) /var/log/lastlog
%ghost %config(noreplace) /etc/hostname
%ghost %config(noreplace) /etc/localtime
%ghost %config(noreplace) /etc/locale.conf
%ghost %config(noreplace) %attr(0444,root,root) /etc/machine-id
%ghost %config(noreplace) /etc/machine-info
%verify(owner group) %config(noreplace) %{_sysconfdir}/rc.d/rc.local
%{_sysconfdir}/rc.local
%ghost %dir %attr(0700,root,root) /var/cache/private
%ghost %dir %attr(0700,root,root) /var/lib/private
%ghost %dir /var/lib/private/systemd
%ghost %dir /var/lib/private/systemd/journal-upload
%ghost /var/lib/private/systemd/journal-upload/state
%ghost %dir /var/lib/systemd/backlight
%ghost /var/lib/systemd/catalog/database
%ghost %dir /var/lib/systemd/coredump
%ghost /var/lib/systemd/journal-upload
%ghost %dir /var/lib/systemd/linger
%ghost %attr(0600,root,root) /var/lib/systemd/random-seed
%ghost %dir /var/lib/systemd/rfkill
%ghost %verify (not mode group md5 mtime) %dir /var/log/journal
%ghost %dir /var/log/journal/remote
%ghost %dir %attr(0700,root,root) /var/log/private
EOF

%check
# Add --num-processes 1 as workaround for issues on ppc64le - AttributeError: 'NoneType' object has no attribute '_add_reader' - https://github.com/python/cpython/issues/82200
%meson_test --num-processes 1

#############################################################################################

%include %{SOURCE1}

%pre
getent group cdrom &>/dev/null || groupadd -r -g 11 cdrom &>/dev/null || :
getent group utmp &>/dev/null || groupadd -r -g 22 utmp &>/dev/null || :
getent group tape &>/dev/null || groupadd -r -g 33 tape &>/dev/null || :
getent group dialout &>/dev/null || groupadd -r -g 18 dialout &>/dev/null || :
getent group input &>/dev/null || groupadd -r input &>/dev/null || :
getent group kvm &>/dev/null || groupadd -r -g 36 kvm &>/dev/null || :
getent group render &>/dev/null || groupadd -r render &>/dev/null || :
getent group systemd-journal &>/dev/null || groupadd -r -g 190 systemd-journal 2>&1 || :

getent group systemd-coredump &>/dev/null || groupadd -r systemd-coredump 2>&1 || :
getent passwd systemd-coredump &>/dev/null || useradd -r -l -g systemd-coredump -d / -s /sbin/nologin -c "systemd Core Dumper" systemd-coredump &>/dev/null || :

getent group systemd-resolve &>/dev/null || groupadd -r -g 193 systemd-resolve 2>&1 || :
getent passwd systemd-resolve &>/dev/null || useradd -r -u 193 -l -g systemd-resolve -d / -s /sbin/nologin -c "systemd Resolver" systemd-resolve &>/dev/null || :

%post
systemd-machine-id-setup &>/dev/null || :
systemctl daemon-reexec &>/dev/null || :
journalctl --update-catalog &>/dev/null || :
systemd-tmpfiles --create &>/dev/null || :

# Make sure new journal files will be owned by the "systemd-journal" group
chgrp systemd-journal /run/log/journal/ /run/log/journal/`cat /etc/machine-id 2>/dev/null` /var/log/journal/ /var/log/journal/`cat /etc/machine-id 2>/dev/null` &>/dev/null || :
chmod g+s /run/log/journal/ /run/log/journal/`cat /etc/machine-id 2>/dev/null` /var/log/journal/ /var/log/journal/`cat /etc/machine-id 2>/dev/null` &>/dev/null || :

# Apply ACL to the journal directory
setfacl -Rnm g:wheel:rx,d:g:wheel:rx,g:adm:rx,d:g:adm:rx /var/log/journal/ &>/dev/null || :

# Stop-gap until rsyslog.rpm does this on its own. (This is supposed
# to fail when the link already exists)
ln -s /usr/lib/systemd/system/rsyslog.service /etc/systemd/system/syslog.service &>/dev/null || :

# Remove spurious /etc/fstab entries from very old installations
# https://bugzilla.redhat.com/show_bug.cgi?id=1009023
if [ -e /etc/fstab ]; then
   grep -v -E -q '^(devpts|tmpfs|sysfs|proc)' /etc/fstab || \
         sed -i.rpm.bak -r '/^devpts\s+\/dev\/pts\s+devpts\s+defaults\s+/d; /^tmpfs\s+\/dev\/shm\s+tmpfs\s+defaults\s+/d; /^sysfs\s+\/sys\s+sysfs\s+defaults\s+/d; /^proc\s+\/proc\s+proc\s+defaults\s+/d' /etc/fstab || :
fi

# We reset the enablement of all services upon initial installation
# https://bugzilla.redhat.com/show_bug.cgi?id=1118740#c23
# This will fix up enablement of any preset services that got installed
# before systemd due to rpm ordering problems:
# Fedora: https://bugzilla.redhat.com/show_bug.cgi?id=1647172
# RHEL: https://bugzilla.redhat.com/show_bug.cgi?id=1783263
if [ $1 -eq 1 ] ; then
        systemctl preset-all &>/dev/null || :
fi

# remove obsolete systemd-readahead file
rm -f /.readahead &>/dev/null || :

%preun
if [ $1 -eq 0 ] ; then
        systemctl disable --quiet \
                remote-fs.target \
                getty@.service \
                serial-getty@.service \
                console-getty.service \
                debug-shell.service \
                systemd-readahead-replay.service \
                systemd-readahead-collect.service \
                systemd-resolved.service \
                >/dev/null || :

        rm -f /etc/systemd/system/default.target &>/dev/null || :
fi

%post libs
%{?ldconfig}

function mod_nss() {
    if [ -f "$1" ] ; then
        # sed-fu to add myhostname to hosts line
        grep -E -q '^hosts:.* myhostname' "$1" ||
        sed -i.bak -e '
                /^hosts:/ !b
                /\<myhostname\>/ b
                s/[[:blank:]]*$/ myhostname/
                ' "$1" &>/dev/null || :

        # Add nss-systemd to passwd and group
        grep -E -q '^(passwd|group):.* systemd' "$1" ||
        sed -i.bak -r -e '
                s/^(passwd|group):(.*)/\1: \2 systemd/
                ' "$1" &>/dev/null || :
    fi
}

FILE="$(readlink /etc/nsswitch.conf || echo /etc/nsswitch.conf)"
if [ "$FILE" = "/etc/authselect/nsswitch.conf" ] && authselect check &>/dev/null; then
        mod_nss "/etc/authselect/user-nsswitch.conf"
        authselect apply-changes &> /dev/null || :
else
        mod_nss "$FILE"
        # also apply the same changes to user-nsswitch.conf to affect
        # possible future authselect configuration
        mod_nss "/etc/authselect/user-nsswitch.conf"
fi

# check if nobody or nfsnobody is defined
export SYSTEMD_NSS_BYPASS_SYNTHETIC=1
if getent passwd nfsnobody &>/dev/null; then
   test -f /etc/systemd/dont-synthesize-nobody || {
       echo 'Detected system with nfsnobody defined, creating /etc/systemd/dont-synthesize-nobody'
       mkdir -p /etc/systemd || :
       : >/etc/systemd/dont-synthesize-nobody || :
   }
elif getent passwd nobody 2>/dev/null | grep -v 'nobody:[x*]:65534:65534:.*:/:/sbin/nologin' &>/dev/null; then
   test -f /etc/systemd/dont-synthesize-nobody || {
       echo 'Detected system with incompatible nobody defined, creating /etc/systemd/dont-synthesize-nobody'
       mkdir -p /etc/systemd || :
       : >/etc/systemd/dont-synthesize-nobody || :
   }
fi

%{?ldconfig:%postun libs -p %ldconfig}

%global udev_services systemd-udev{d,-settle,-trigger}.service systemd-udevd-{control,kernel}.socket

%post udev
# Move old stuff around in /var/lib
mv %{_localstatedir}/lib/random-seed %{_localstatedir}/lib/systemd/random-seed &>/dev/null
mv %{_localstatedir}/lib/backlight %{_localstatedir}/lib/systemd/backlight &>/dev/null

udevadm hwdb --update &>/dev/null
%systemd_post %udev_services
/usr/lib/systemd/systemd-random-seed save 2>&1

# Replace obsolete keymaps
# https://bugzilla.redhat.com/show_bug.cgi?id=1151958
grep -q -E '^KEYMAP="?fi-latin[19]"?' /etc/vconsole.conf 2>/dev/null &&
    sed -i.rpm.bak -r 's/^KEYMAP="?fi-latin[19]"?/KEYMAP="fi"/' /etc/vconsole.conf || :

%postun udev
# Only restart systemd-udev, to run the upgraded dameon.
# Others are either oneshot services, or sockets, and restarting them causes issues (#1378974)
%systemd_postun_with_restart systemd-udevd.service

%pre journal-remote
getent group systemd-journal-remote &>/dev/null || groupadd -r systemd-journal-remote 2>&1 || :
getent passwd systemd-journal-remote &>/dev/null || useradd -r -l -g systemd-journal-remote -d %{_localstatedir}/log/journal/remote -s /sbin/nologin -c "Journal Remote" systemd-journal-remote &>/dev/null || :

%post journal-remote
%systemd_post systemd-journal-gatewayd.socket systemd-journal-gatewayd.service
%systemd_post systemd-journal-remote.socket systemd-journal-remote.service
%systemd_post systemd-journal-upload.service
%firewalld_reload

%preun journal-remote
%systemd_preun systemd-journal-gatewayd.socket systemd-journal-gatewayd.service
%systemd_preun systemd-journal-remote.socket systemd-journal-remote.service
%systemd_preun systemd-journal-upload.service
if [ $1 -eq 1 ] ; then
    if [ -f %{_localstatedir}/lib/systemd/journal-upload/state -a ! -L %{_localstatedir}/lib/systemd/journal-upload ] ; then
        mkdir -p %{_localstatedir}/lib/private/systemd/journal-upload
        mv %{_localstatedir}/lib/systemd/journal-upload/state %{_localstatedir}/lib/private/systemd/journal-upload/.
        rmdir %{_localstatedir}/lib/systemd/journal-upload || :
    fi
fi

%postun journal-remote
%systemd_postun_with_restart systemd-journal-gatewayd.service
%systemd_postun_with_restart systemd-journal-remote.service
%systemd_postun_with_restart systemd-journal-upload.service
%firewalld_reload

%global _docdir_fmt %{name}

%files -f %{name}.lang -f .file-list-rest
%doc %{_pkgdocdir}
%exclude %{_pkgdocdir}/LICENSE.*
%license LICENSE.GPL2 LICENSE.LGPL2.1
%ghost %dir %attr(0755,-,-) /etc/systemd/system/basic.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/bluetooth.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/default.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/getty.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/graphical.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/local-fs.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/machines.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/multi-user.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/printer.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/remote-fs.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/sockets.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/sysinit.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/system-update.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/timers.target.wants
%ghost %dir %attr(0755,-,-) /var/lib/rpm-state/systemd

%files libs -f .file-list-libs
%license LICENSE.LGPL2.1

%files pam -f .file-list-pam

%files devel -f .file-list-devel

%files udev -f .file-list-udev

%files container -f .file-list-container

%files journal-remote -f .file-list-remote

%files tests -f .file-list-tests

%changelog
* Wed Jun 28 2023 Release Engineering <releng@rockylinux.org> - 239-74
- Remove support URL patch

* Thu May 18 2023 systemd maintenance team <systemd-maint@redhat.com> - 239-74.2
- pstore: fix crash and forward dummy arguments instead of NULL (#2190153)
- ci: workflow for gathering metadata for source-git automation (#2190153)
- ci: first part of the source-git automation - commit linter (#2190153)

* Tue Apr 18 2023 systemd maintenance team <systemd-maint@redhat.com> - 239-74.1
- pager: set $LESSSECURE whenver we invoke a pager (#2175623)
- test-login: always test sd_pid_get_owner_uid(), modernize (#2175623)
- pager: make pager secure when under euid is changed or explicitly requested (#2175623)
- test: ignore ENOMEDIUM error from sd_pid_get_cgroup() (#2175623)

* Tue Mar 14 2023 systemd maintenance team <systemd-maint@redhat.com> - 239-74
- journald-server: always create state file in signal handler (#2174645)
- journald-server: move relinquish code into function (#2174645)
- journald-server: always touch state file in signal handler (#2174645)

* Mon Feb 27 2023 systemd maintenance team <systemd-maint@redhat.com> - 239-73
- journald: add API to move logging from /var to /run again (#1873540)
- journalctl: add new --relinquish and --smart-relinquish options (#1873540)
- units: automatically revert to /run logging on shutdown if necessary (#1873540)
- pstore: Tool to archive contents of pstore (#2158832)
- meson: drop redundant line (#2158832)
- pstore: drop unnecessary initializations (#2158832)
- pstopre: fix return value of list_files() (#2158832)
- pstore: remove temporary file on failure (#2158832)
- pstore: do not add FILE= journal entry if content_size == 0 (#2158832)
- pstore: run only when /sys/fs/pstore is not empty (#2158832)
- pstore: fix use after free (#2158832)
- pstore: refuse to run if arguments are specified (#2158832)
- pstore: allow specifying src and dst dirs are arguments (#2158832)
- pstore: rework memory handling for dmesg (#2158832)
- pstore: fixes for dmesg.txt reconstruction (#2158832)
- pstore: Don't start systemd-pstore.service in containers (#2158832)
- units: pull in systemd-pstore.service from sysinit.target (#2158832)
- units: drop dependency on systemd-remount-fs.service from systemd-pstore.service (#2158832)
- units: make sure systemd-pstore stops at shutdown (#2158832)
- pstore: Run after modules are loaded (#2158832)
- pstore: do not try to load all known pstore modules (#2158832)
- logind-session: make stopping of idle session visible to admins (#2156780)
- journald: Increase stdout buffer size sooner, when almost full (#2029426)
- journald: rework end of line marker handling to use a field table (#2029426)
- journald: use the fact that client_context_release() returns NULL (#2029426)
- journald: rework pid change handling (#2029426)
- test: Add a test case for #15654 (#2029426)
- test: Stricter test case for #15654 (Add more checks) (#2029426)
- man: document the new _LINE_BREAK= type (#2029426)

* Fri Feb 17 2023 systemd maintenance team <systemd-maint@redhat.com> - 239-72
- test: import logind test from debian/ubuntu test suite (#1866955)
- test: introduce inst_recursive() helper function (#1866955)
- tests: verify that Lock D-Bus signal is sent when IdleAction=lock (#1866955)
- systemctl: simplify halt_main() (#2053273)
- systemctl: shutdown don't fallback on auth fail (#2053273)
- systemctl: reintroduce the original halt_main() (#2053273)
- systemctl: preserve old behavior unless requested (#2053273)
- pam_systemd: suppress LOG_DEBUG log messages if debugging is off (#2170084)
- udev/net_id: introduce naming scheme for RHEL-8.8 (#2170499)
- pam: add a call to pam_namespace (#1861836)

* Tue Jan 31 2023 systemd maintenance team <systemd-maint@redhat.com> - 239-71
- manager: limit access to private dbus socket (#2119405)
- journalctl: do not treat EINTR as an error when waiting for events (#2161683)
- core: bring manager_startup() and manager_reload() more inline (#2059633)
- pam: add a call to pam_namespace (#1861836)
- virt: Support detection for ARM64 Hyper-V guests (#2158307)
- virt: Fix the detection for Hyper-V VMs (#2158307)
- basic: add STRERROR() wrapper for strerror_r() (#2155520)
- coredump: put context array into a struct (#2155520)
- coredump: do not allow user to access coredumps with changed uid/gid/capabilities (#2155520)

* Mon Jan 16 2023 systemd maintenance team <systemd-maint@redhat.com> - 239-70
- basic: recognize pdfs filesystem as a network filesystem (#2094661)
- core: move reset_arguments() to the end of main's finish (#2127131)
- manager: move inc. of n_reloading into a function (#2136869)
- core: Add new DBUS properties UnitsReloadStartTimestamp and UnitsLoadTimestampMontonic (#2136869)
- core: Indicate the time when the manager started loading units the last time (#2136869)
- core: do not touch /run/systemd/systemd-units-load from user session instances (#2136869)
- sysctl: downgrade message when we have no permission (#2158160)
- core: respect SELinuxContext= for socket creation (#2136738)
- manager: use target process context to set socket context (#2136738)
- virt: detect Amazon EC2 Nitro instance (#2117948)
- machine-id-setup: generate machine-id from DMI product ID on Amazon EC2 (#2117948)
- virt: use string table to detect VM or container (#2117948)
- fileio: introduce read_full_virtual_file() for reading virtual files in sysfs, procfs (#2117948)
- Use BIOS characteristics to distinguish EC2 bare-metal from VMs (#2117948)
- device: drop refuse_after (#2043524)

* Tue Nov 08 2022 systemd maintenance team <systemd-maint@redhat.com> - 239-69
- logind: optionally watch utmp for login data (#2122288)
- logind: add hashtable for finding session by leader PID (#2122288)
- core/load-fragment: move config_parse_sec_fix_0 to src/shared (#2122288)
- sd-event: add relative timer calls (#2122288)
- logind: add option to stop idle sessions after specified timeout (#2122288)
- logind: schedule idle check full interval from now if we couldn't figure out atime timestamp (#2122288)
- ci(lint): add shell linter - Differential ShellCheck (#2122499)
- meson: do not compare objects of different types (#2122499)
- journal-remote: use MHD_HTTP_CONTENT_TOO_LARGE as MHD_HTTP_PAYLOAD_TOO_LARGE is deprecated since 0.9.74 (#2122499)
- Fix build with µhttpd 0.9.71 (#2122499)
- ci: replace LGTM with CodeQL (#2122499)
- ci(mergify): Update policy - Drop LGTM checks (#2122499)
- time-util: fix buffer-over-run (#2139391)

* Fri Aug 26 2022 systemd maintenance team <systemd-maint@redhat.com> - 239-67
- resolved: pin stream while calling callbacks for it (#2110549)
- ci(functions): Add `useradd` and `userdel` (#2110549)

* Thu Aug 25 2022 systemd maintenance team <systemd-maint@redhat.com> - 239-66
- Try stopping MD RAID devices in shutdown too (#1817706)
- shutdown: get only active md arrays. (#1817706)
- scope: allow unprivileged delegation on scopes (#2068575)

* Fri Aug 19 2022 systemd maintenance team <systemd-maint@redhat.com> - 239-65
- test-procfs-util: skip test on certain errors (#2087152)

* Thu Aug 18 2022 systemd maintenance team <systemd-maint@redhat.com> - 239-64
- ci: bump the worker Ubuntu version to Jammy (#2087152)
- test: make test-execute pass on Linux 5.15 (#2087152)
- ci: install iputils (#2087152)
- ci(Mergify): Add `ci-waived` logic (#2087152)
- sd-event: don't invalidate source type on disconnect (#2115396)
- tests: make sure we delay running mount start jobs when /p/s/mountinfo is rate limited (#2095744)
- core: drop references to 'StandardOutputFileToCreate' (#2093479)
- dbus-execute: fix indentation (#2093479)
- dbus-execute: generate the correct transient unit setting (#2093479)
- bus-unit-util: properly accept StandardOutput=append:… settings (#2093479)
- core: be more careful when inheriting stdout fds to stderr (#2093479)
- test: add a test for StandardError=file:… (#2093479)
- tree-wide: allow ASCII fallback for → in logs (#2093479)
- tree-wide: allow ASCII fallback for … in logs (#2093479)
- core: allow to set default timeout for devices (#1967245)
- man: document DefaultDeviceTimeoutSec= (#1967245)
- Revert "core: Propagate condition failed state to triggering units." (#2114005)
- core: Check unit start rate limiting earlier (#2114005)
- core: Add trigger limit for path units (#2114005)
- meson: add syscall-names-update target (#2040247)
- syscall-names: add process_madvise which is planned for 5.10 (#2040247)
- shared: add @known syscall list (#2040247)
- generate-syscall-list: require python3 (#2040247)
- shared/seccomp: reduce scope of indexing variables (#2040247)
- shared/syscall-list: filter out some obviously platform-specific syscalls (#2040247)
- seccomp: tighten checking of seccomp filter creation (#2040247)
- shared/seccomp-util: added functionality to make list of filtred syscalls (#2040247)
- nspawn: return ENOSYS by default, EPERM for "known" calls (#2040247)
- revert: resolved: pin stream while calling callbacks for it (#2110549)

* Wed Aug 03 2022 systemd maintenance team <systemd-maint@redhat.com> - 239-63
- resolved: pin stream while calling callbacks for it (#2110549)

* Mon Jul 18 2022 systemd maintenance team <systemd-maint@redhat.com> - 239-62
- spec: Remove dependency on timedatex (#2066946)

* Thu Jul 14 2022 systemd maintenance team <systemd-maint@redhat.com> - 239-61
- mkosi: Add gnutls package (#2101227)
- unit-name: tighten checks for building valid unit names (#1940973)
- core: shorten long unit names that are based on paths and append path hash at the end (#1940973)
- test: add extended test for triggering mount rate limit (#1940973)
- tests: add test case for long unit names (#1940973)
- core: unset HOME=/ that the kernel gives us (#2056527)
- journal-remote: check return value from MHD_add_response_header (#2051981)
- journalctl: in --follow mode watch stdout for POLLHUP/POLLERR and exit (#2003236)
- sd-bus: make BUS_DEFAULT_TIMEOUT configurable (#2039461)
- fstab-generator: fix debug log (#2101433)
- logind-session-dbus: allow to set display name via dbus (#1857969)
- Allow restart for oneshot units (#2042896)
- test: correct TEST-41 StartLimitBurst test (#2042896)
- core: fix assert() about number of built environment variables (#2049788)
- core: add one more assert() (#2049788)
- strv: introduce strv_join_prefix() (#2049788)
- test: add tests for strv_join_prefix() (#2049788)
- test: replace swear words by 'hoge' (#2049788)
- core: add new environment variable $RUNTIME_DIRECTORY= or friends (#2049788)
- test-execute: add tests for $RUNTIME_DIRECTORY= or friends (#2049788)
- man: document RUNTIME_DIRECTORY= or friends (#2049788)

* Thu Jun 23 2022 systemd maintenance team <systemd-maint@redhat.com> - 239-60
- unit: don't emit PropertiesChanged signal if adding a dependency to a unit is a no-op (#1948480)
- tests: make inverted tests actually count (#2087152)
- TEST-*: make failure tests actually fail on failure (#2087152)
- ci(Mergify): configuration update (#2087152)
- core: propagate triggered unit in more load states (#2065322)
- core: propagate unit start limit hit state to triggering path unit (#2065322)
- core: Move 'r' variable declaration to start of unit_start() (#2065322)
- core: Delay start rate limit check when starting a unit (#2065322)
- core: Propagate condition failed state to triggering units. (#2065322)
- unit: check for mount rate limiting before checking active state (#2095744)

* Wed May 18 2022 systemd maintenance team <systemd-maint@redhat.com> - 239-59
- core: disallow using '-.service' as a service name (#2051520)
- shared/dropin: support -.service.d/ top level drop-in for service units (#2051520)
- core: change top-level drop-in from -.service.d to service.d (#2051520)
- shared/dropin: fix assert for invalid drop-in (#2051520)
- udev: fix slot based network names on s390 (#1939914)
- udev: it is not necessary that the path is readable (#1939914)
- udev: allow onboard index up to 65535 (#1939914)
- Revert "basic: use comma as separator in cpuset cgroup cpu ranges" (#1858220)
- acpi-fpdt: mark structures as packed (#2047373)
- core/slice: make slice_freezer_action() return 0 if freezing state is unchanged (#2047373)
- core/unit: fix use-after-free (#2047373)
- sd-bus: fix reference counter to be incremented (#2047373)
- sd-bus: do not read unused value (#2047373)
- sd-bus: do not return negative errno when unknown name is specified (#2047373)
- sd-bus: switch to a manual overflow check in sd_bus_track_add_name() (#2047373)
- spec: Add dependency on timedatex (#2066946)

* Tue Feb 08 2022 systemd maintenance team <systemd-maint@redhat.com> - 239-58
- ci: drop CentOS 8 CI (#2017033)
- test: adapt to the new capsh format (#2017033)
- test: ignore IAB capabilities in `test-execute` (#2017033)

* Mon Feb 07 2022 systemd maintenance team <systemd-maint@redhat.com> - 239-57
- udev/net_id: introduce naming scheme for RHEL-8.5 (#2039797)
- udev/net_id: remove extraneous bracket (#2039797)
- udev/net_id: introduce naming scheme for RHEL-8.6 (#2039797)
- define newly needed constants (#2005008)
- sd-netlink: support IFLA_PROP_LIST and IFLA_ALT_IFNAME attributes (#2005008)
- sd-netlink: introduce sd_netlink_message_read_strv() (#2005008)
- sd-netlink: introduce sd_netlink_message_append_strv() (#2005008)
- test: add a test for sd_netlink_message_{append,read}_strv() (#2005008)
- util: introduce ifname_valid_full() (#2005008)
- rename function (#2005008)
- udev: support AlternativeName= setting in .link file (#2005008)
- network: make Name= in [Match] support alternative names of interfaces (#2005008)
- udev: extend the length of ID_NET_NAME_XXX= to ALTIFNAMSIZ (#2005008)
- udev: do not fail if kernel does not support alternative names (#2005008)
- udev: introduce AlternativeNamesPolicy= setting (#2005008)
- network: set AlternativeNamesPolicy= in 99-default.link (#2005008)
- random-util: call initialize_srand() after fork() (#2005008)
- sd-netlink: introduce rtnl_resolve_link_alternative_names() (#2005008)
- udev: sort alternative names (#2005008)
- netlink: introduce rtnl_get/delete_link_alternative_names() (#2005008)
- netlink: do not fail when new interface name is already used as an alternative name (#2005008)
- udev: do not try to reassign alternative names (#2005008)
- Do not fail if the same alt. name is set again (#2005008)
- mount: do not update exec deps on mountinfo changes (#2008825)
- core/mount: add implicit unit dependencies even if when mount unit is generated from /proc/self/mountinfo (#2008825)
- core: fix unfortunate typo in unit_is_unneeded() (#2040147)
- core: make destructive transaction error a bit more useful (#2040147)
- tmpfiles: use a entry in hashmap as ItemArray in read_config_file() (#1944468)
- tmpfiles: rework condition check (#1944468)
- TEST-22-TMPFILES: add reproducer for bug with X (#1944468)
- core: make sure we don't get confused when setting TERM for a tty fd (#2045307)
- hash-funcs: introduce macro to create typesafe hash_ops (#2037807)
- hash-func: add destructors for key and value (#2037807)
- util: define free_func_t (#2037807)
- hash-funcs: make basic hash_ops typesafe (#2037807)
- test: add tests for destructors of hashmap or set (#2037807)
- man: document the new sysctl.d/ - prefix (#2037807)
- sysctl: if options are prefixed with "-" ignore write errors (#2037807)
- sysctl: fix segfault (#2037807)

* Tue Jan 25 2022 systemd maintenance team <systemd-maint@redhat.com> - 239-56
- Take ghost ownership of /var/log/lastlog (#1798685)

* Mon Jan 10 2022 systemd maintenance team <systemd-maint@redhat.com> - 239-55
- lgtm: detect uninitialized variables using the __cleanup__ attribute (#2017033)
- lgtm: replace the query used for looking for fgets with a more general query (#2017033)
- lgtm: beef up list of dangerous/questionnable API calls not to make (#2017033)
- lgtm: warn about strerror() use (#2017033)
- lgtm: complain about accept() [people should use accept4() instead, due to O_CLOEXEC] (#2017033)
- lgtm: don't treat the custom note as a list of tags (#2017033)
- lgtm: ignore certain cleanup functions (#2017033)
- lgtm: detect more possible problematic scenarios (#2017033)
- lgtm: enable more (and potentially useful) queries (#2017033)
- test: make TEST-47 less racy (#2017033)
- core: rename unit_{start_limit|condition|assert}_test() to unit_test_xyz() (#2036608)
- core: Check unit start rate limiting earlier (#2036608)
- sd-event: introduce callback invoked when event source ratelimit expires (#2036608)
- core: rename/generalize UNIT(u)->test_start_limit() hook (#2036608)
- mount: make mount units start jobs not runnable if /p/s/mountinfo ratelimit is in effect (#2036608)
- mount: retrigger run queue after ratelimit expired to run delayed mount start jobs (#2036608)
- pid1: add a manager_trigger_run_queue() helper (#2036608)
- unit: add jobs that were skipped because of ratelimit back to run_queue (#2036608)
- Revert "Revert "sysctl: Enable ping(8) inside rootless Podman containers"" (#2037807)
- sysctl: prefix ping port range setting with a dash (#2037807)
- mount: don't propagate errors from mount_setup_unit() further up (#2036853)

* Wed Dec 01 2021 systemd maintenance team <systemd-maint@redhat.com> - 239-54
- core: consider service with no start command immediately started (#1860899)
- man: move description of *Action= modes to FailureAction=/SuccessAction= (#1860899)
- core: define "exit" and "exit-force" actions for user units and only accept that (#1860899)
- core: accept system mode emergency action specifiers with a warning (#1860899)
- core: allow services with no commands but SuccessAction set (#1860899)
- core: limit service-watchdogs=no to actual "watchdog" commands (#1860899)
- units: use SuccessAction=exit-force in systemd-exit.service (#1860899)
- units: use SuccessAction=reboot-force in systemd-reboot.service (#1860899)
- units: use SuccessAction=poweroff-force in systemd-poweroff.service (#1860899)
- units: allow and use SuccessAction=exit-force in system systemd-exit.service (#1860899)
- core: do not "warn" about mundane emergency actions (#1860899)
- core: return true from cg_is_empty* on ENOENT (#1860899)
- macro: define HAS_FEATURE_ADDRESS_SANITIZER also on gcc (#2017033)
- tests: add helper function to autodetect CI environments (#2017033)
- strv: rework FOREACH_STRING() macro (#2017033)
- test,systemctl: use "const char*" instead of "char*" (#2017033)
- ci: pass the $GITHUB_ACTIONS variable to the CentOS container (#2017033)

* Wed Nov 24 2021 systemd maintenance team <systemd-maint@redhat.com> - 239-53
- sd-hwdb: allow empty properties (#2005009)
- Update hwdb (#2005009)
- Disable libpitc to fix CentOS Stream CI (#2017033)
- rpm: Fix typo in %_environmentdir (#2018024)
- rpm: Add misspelled %_environmentdir macro for temporary compatibility (#2018024)
- rpm: emit warning when macro with typo is used (#2018024)
- Remove unintended additions to systemd-analyze man page (#2004765)
- core: fix SIGABRT on empty exec command argv (#2020239)
- core/service: also check path in exec commands (#2020239)
- mount-util: fix fd_is_mount_point() when both the parent and directory are network fs (#2015057)
- basic: add vmware hypervisor detection from device-tree (#1959150)
- pam: do not require a non-expired password for user@.service (#1961746)
- udev rules: add rule to create /dev/ptp_hyperv (#1991834)
- process-util: explicitly handle processes lacking parents in get_process_ppid() (#1977569)
- errno-util: add ERRNO_IS_PRIVILEGE() helper (#1977569)
- procfs-util: fix confusion wrt. quantity limit and maximum value (#1977569)
- test-process-util: also add EROFS to the list of "good" errors (#1977569)
- journal: refresh cached credentials of stdout streams (#1931806)
- util-lib: introduce HAS_FEATURE_ADDRESS_SANITIZER (#2017033)
- ci: skip test-execute on GH Actions under ASan (#2017033)
- test-seccomp: accept ENOSYS from sysctl(2) too (#2017033)
- test: accept that char device 0/0 can now be created witout privileges (#2017033)
- meson: do not fail if rsync is not installed with meson 0.57.2 (#2017033)
- pid1: fix free of uninitialized pointer in unit_fail_if_noncanonical() (#1970945)
- sd-event: take ref on event loop object before dispatching event sources (#1970945)

* Fri Aug 27 2021 systemd maintenance team <systemd-maint@redhat.com> - 239-50
- Added option --check-inhibitors for non-tty usage (#1269726)
- logind: Introduce RebootWithFlags and others (#1269726)
- logind: add …WithFlags methods to policy (#1269726)
- logind: simplify flags handling a bit (#1269726)
- Update link to RHEL documentation (#1982584)
- Set default core ulimit to 0, but keep the hard limit ulimited (#1905582)
- shared/seccomp-util: address family filtering is broken on ppc (#1982650)
- logind: rework Seat/Session/User object allocation and freeing a bit (#1642460)
- logind: fix serialization/deserialization of user's "display session" (#1642460)
- logind: turn of stdio locking when writing session files too (#1642460)
- units: set StopWhenUnneeded= for the user slice units too (#1642460)
- units: improve Description= string a bit (#1642460)
- logind: improve logging in manager_connect_console() (#1642460)
- logind: save/restore User object's "stopping" field during restarts (#1642460)
- logind: correct bad clean-up path (#1642460)
- logind: fix bad error propagation (#1642460)
- logind: never elect a session that is stopping as display (#1642460)
- logind: introduce little helper that checks whether a session is ready (#1642460)
- logind: propagate session stop errors (#1642460)
- logind: rework how we manage the slice and user-runtime-dir@.service unit for each user (#1642460)
- logind: optionally, keep the user@.service instance for eached logged in user around for a while (#1642460)
- logind: add a RequiresMountsFor= dependency from the session scope unit to the home directory of the user (#1642460)
- logind: improve error propagation of user_check_linger_file() (#1642460)
- logind: automatically GC lingering users for who now user@.service (nor slice, not runtime dir service) is running anymore (#1642460)
- pam_systemd: simplify code which with we set environment variables (#1642460)
- logind: validate /run/user/1000 before we set it (#1642460)

* Fri Jul 23 2021 systemd maintenance team <systemd-maint@redhat.com> - 239-49
- remove a left-over break (#1970860)
- basic/unit-name: do not use strdupa() on a path (#1974700)
- sd-event: change ordering of pending/ratelimited events (#1968528)
- sd-event: drop unnecessary "else" (#1968528)
- sd-event: use CMP() macro (#1968528)
- sd-event: use usec_add() (#1968528)
- sd-event: make event_source_time_prioq_reshuffle() accept all event source type (#1968528)
- sd-event: always reshuffle time prioq on changing online/offline state (#1968528)
- ci: run unit tests on z-stream branches as well (#1970860)
- ci: drop forgotten Travis references (#1934504)
- ci: run unit tests on CentOS 8 Stream as well (#1934504)
- ci: add missing test dependencies (#1934504)
- meson: bump timeout for test-udev to 180s (#1934504)

* Thu Jun 24 2021 systemd maintenance team <systemd-maint@redhat.com> - 239-48
- cgroup: Also set io.bfq.weight (#1927290)
- seccomp: allow turning off of seccomp filtering via env var (#1916835)
- meson: remove strange dep that causes meson to enter infinite loop (#1970860)
- copy: handle copy_file_range() weirdness on procfs/sysfs (#1970860)
- core: Hide "Deactivated successfully" message (#1954802)
- util: rework in_initrd() to make use of path_is_temporary_fs() (#1959339)
- initrd: extend SYSTEMD_IN_INITRD to accept non-ramfs rootfs (#1959339)
- initrd: do a debug log if failed to detect rootfs type (#1959339)
- initrd: do a debug log if /etc/initrd-release doesn't take effect (#1959339)
- units: assign user-runtime-dir@.service to user-%i.slice (#1946453)
- units: order user-runtime-dir@.service after systemd-user-sessions.service (#1946453)
- units: make sure user-runtime-dir@.service is Type=oneshot (#1946453)
- user-runtime-dir: downgrade a few log messages to LOG_DEBUG that we ignore (#1946453)
- shared/install: Preserve escape characters for escaped unit names (#1952686)
- basic/virt: Detect PowerVM hypervisor (#1937989)
- man: document differences in clean exit status for Type=oneshot (#1940078)
- busctl: add a timestamp to the output of the busctl monitor command (#1909214)
- basic/cap-list: parse/print numerical capabilities (#1946943)
- shared/mount-util: convert to libmount (#1885143)
- mount-util: bind_remount: avoid calling statvfs (#1885143)
- mount-util: use UMOUNT_NOFOLLOW in recursive umounter (#1885143)
- test-install-root: create referenced targets (#1835351)
- install: warn if WantedBy targets don't exist (#1835351)
- test-install-root: add test for unknown WantedBy= target (#1835351)
- ceph is a network filesystem (#1952013)
- sysctl: set kernel.core_pipe_limit=16 (#1949729)
- core: don't drop timer expired but not yet processed when system date is changed (#1899402)
- core: Detect initial timer state from serialized data (#1899402)
- rc-local: order after network-online.target (#1934028)
- set core ulimit to 0 like on RHEL-7 (#1905582)
- test-mountpointutil-util: do not assert in test_mnt_id() (#1910425)

* Fri Jun 04 2021 Jan Macku <jamacku@redhat.com> - 239-47
- systemd-binfmt: Add safeguard in triggers (#1787144)
- spec: Requires(post) openssl-libs to fix missing /etc/machine-id (#1947438)
- spec: Go back to using systemctl preset-all in post (#1783263, #1647172, #1118740)
- spec: Disable libiptc support (#1817265)

* Wed May 19 2021 systemd maintenance team <systemd-maint@redhat.com> - 239-46
- Revert "udev: run link_update() with increased retry count in second invocation" (#1942299)
- Revert "udev: make algorithm that selects highest priority devlink less susceptible to race conditions" (#1942299)
- test/udev-test.pl: drop test cases that add mutliple devices (#1942299)

* Thu Mar 11 2021 systemd maintenance team <systemd-maint@redhat.com> - 239-45
- Revert "test: add test cases for empty string match" and "test: add test case for multi matches when use ||" (#1935124)
- test/sys-script.py: add missing DEVNAME entries to uevents (#1935124)
- sd-event: split out helper functions for reshuffling prioqs (#1937315)
- sd-event: split out enable and disable codepaths from sd_event_source_set_enabled() (#1937315)
- sd-event: mention that two debug logged events are ignored (#1937315)
- sd-event: split clock data allocation out of sd_event_add_time() (#1937315)
- sd-event: split out code to add/remove timer event sources to earliest/latest prioq (#1937315)
- sd-event: fix delays assert brain-o (#17790) (#1937315)
- sd-event: let's suffix last_run/last_log with "_usec" (#1937315)
- sd-event: refuse running default event loops in any other thread than the one they are default for (#1937315)
- sd-event: ref event loop while in sd_event_prepare() ot sd_event_run() (#1937315)
- sd-event: follow coding style with naming return parameter (#1937315)
- sd-event: remove earliest_index/latest_index into common part of event source objects (#1937315)
- sd-event: update state at the end in event_source_enable (#1937315)
- sd-event: increase n_enabled_child_sources just once (#1937315)
- sd-event: add ability to ratelimit event sources (#1937315)
- test: add ratelimiting test (#1937315)
- core: prevent excessive /proc/self/mountinfo parsing (#1937315)
- udev: run link_update() with increased retry count in second invocation (#1935124)
- pam-systemd: use secure_getenv() rather than getenv() (#1936866)

* Thu Jan 28 2021 systemd maintenance team <systemd-maint@redhat.com> - 239-44
- ci: PowerTools repo was renamed to powertools in RHEL 8.3 (#1871827)
- ci: use quay.io instead of Docker Hub to avoid rate limits (#1871827)
- ci: move jobs from Travis CI to GH Actions (#1871827)
- unit: make UNIT() cast function deal with NULL pointers (#1871827)
- use link to RHEL-8 docs (#1623116)
- cgroup: Also set blkio.bfq.weight (#1657810)
- units: make sure initrd-cleanup.service terminates before switching to rootfs (#1657810)
- core: reload SELinux label cache on daemon-reload (#1888912)
- selinux: introduce mac_selinux_create_file_prepare_at() (#1888912)
- selinux: add trigger for policy reload to refresh internal selabel cache (#1888912)
- udev/net_id: give RHEL-8.4 naming scheme a name (#1827462)
- basic/stat-util: make mtime check stricter and use entire timestamp (#1642728)
- udev: make algorithm that selects highest priority devlink less susceptible to race conditions (#1642728)
- test: create /dev/null in test-udev.pl (#1642728)
- test: missing "die" (#1642728)
- udev-test: remove a check for whether the test is run in a container (#1642728)
- udev-test: skip the test only if it can't setup its environment (#1642728)
- udev-test: fix test skip condition (#1642728)
- udev-test: fix missing directory test/run (#1642728)
- udev-test: check if permitted to create block device nodes (#1642728)
- test-udev: add a testcase of too long line (#1642728)
- test-udev: use proper semantics for too long line with continuation (#1642728)
- test-udev: add more tests for line continuations and comments (#1642728)
- test-udev: add more tests for line continuation (#1642728)
- test-udev: fix alignment and drop unnecessary white spaces (#1642728)
- test/udev-test.pl: cleanup if skipping test (#1642728)
- test: add test cases for empty string match (#1642728)
- test: add test case for multi matches when use "||" (#1642728)
- udev-test: do not rely on "mail" group being defined (#1642728)
- test/udev-test.pl: allow multiple devices per test (#1642728)
- test/udev-test.pl: create rules only once (#1642728)
- test/udev-test.pl: allow concurrent additions and removals (#1642728)
- test/udev-test.pl: use computed devnode name (#1642728)
- test/udev-test.pl: test correctness of symlink targets (#1642728)
- test/udev-test.pl: allow checking multiple symlinks (#1642728)
- test/udev-test.pl: fix wrong test descriptions (#1642728)
- test/udev-test.pl: last_rule is unsupported (#1642728)
- test/udev-test.pl: Make some tests a little harder (#1642728)
- test/udev-test.pl: remove bogus rules from magic subsys test (#1642728)
- test/udev-test.pl: merge "space and var with space" tests (#1642728)
- test/udev-test.pl: merge import parent tests into one (#1642728)
- test/udev-test.pl: count "good" results (#1642728)
- tests/udev-test.pl: add multiple device test (#1642728)
- test/udev-test.pl: add repeat count (#1642728)
- test/udev-test.pl: generator for large list of block devices (#1642728)
- test/udev-test.pl: suppress umount error message at startup (#1642728)
- test/udev_test.pl: add "expected good" count (#1642728)
- test/udev-test: gracefully exit when imports fail (#1642728)

* Thu Nov 26 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-43
- man: mention System Administrator's Guide in systemctl manpage (#1623116)
- udev: introduce udev net_id "naming schemes" (#1827462)
- meson: make net.naming-scheme= default configurable (#1827462)
- man: describe naming schemes in a new man page (#1827462)
- udev/net_id: parse _SUN ACPI index as a signed integer (#1827462)
- udev/net_id: don't generate slot based names if multiple devices might claim the same slot (#1827462)
- fix typo in ProtectSystem= option (#1871139)
- remove references of non-existent man pages (#1876807)
- log: Prefer logging to CLI unless JOURNAL_STREAM is set (#1865840)
- locale-util: add new helper locale_is_installed() (#1755287)
- test: add test case for locale_is_installed() (#1755287)
- tree-wide: port various bits over to locale_is_installed() (#1755287)
- install: allow instantiated units to be enabled via presets (#1812972)
- install: small refactor to combine two function calls into one function (#1812972)
- test: fix a memleak (#1812972)
- docs: Add syntax for templated units to systemd.preset man page (#1812972)
- shared/install: fix preset operations for non-service instantiated units (#1812972)
- introduce setsockopt_int() helper (#1887181)
- socket-util: add generic socket_pass_pktinfo() helper (#1887181)
- core: add new PassPacketInfo= socket unit property (#1887181)
- resolved: tweak cmsg calculation (#1887181)

* Tue Nov 03 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-42
- logind: don't print warning when user@.service template is masked (#1880270)
- build: use simple project version in pkgconfig files (#1862714)
- basic/virt: try the /proc/1/sched hack also for PID1 (#1868877)
- seccomp: rework how the S[UG]ID filter is installed (#1860374)
- vconsole-setup: downgrade log message when setting font fails on dummy console (#1889996)
- units: fix systemd.special man page reference in system-update-cleanup.service (#1871827)
- units: drop reference to sushell man page (#1871827)
- sd-bus: break the loop in bus_ensure_running() if the bus is not connecting (#1885553)
- core: add new API for enqueing a job with returning the transaction data (#846319)
- systemctl: replace switch statement by table of structures (#846319)
- systemctl: reindent table (#846319)
- systemctl: Only wait when there's something to wait for. (#846319)
- systemctl: clean up start_unit_one() error handling (#846319)
- systemctl: split out extra args generation into helper function of its own (#846319)
- systemctl: add new --show-transaction switch (#846319)
- test: add some basic testing that "systemctl start -T" does something (#846319)
- man: document the new systemctl --show-transaction option (#846319)
- socket: New option 'FlushPending' (boolean) to flush socket before entering listening state (#1870638)
- core: remove support for API bus "started outside our own logic" (#1764282)
- mount-setup: fix segfault in mount_cgroup_controllers when using gcc9 compiler (#1868877)
- dbus-execute: make transfer of CPUAffinity endian safe (#12711) (#1740657)
- core: add support for setting CPUAffinity= to special "numa" value (#1740657)
- basic/user-util: always use base 10 for user/group numbers (#1848373)
- parse-util: sometimes it is useful to check if a string is a valid integer, but not actually parse it (#1848373)
- basic/parse-util: add safe_atoux64() (#1848373)
- parse-util: allow tweaking how to parse integers (#1848373)
- parse-util: allow '-0' as alternative to '0' and '+0' (#1848373)
- parse-util: make return parameter optional in safe_atou16_full() (#1848373)
- parse-util: rewrite parse_mode() on top of safe_atou_full() (#1848373)
- user-util: be stricter in parse_uid() (#1848373)
- strv: add new macro STARTSWITH_SET() (#1848373)
- parse-util: also parse integers prefixed with 0b and 0o (#1848373)
- tests: beef up integer parsing tests (#1848373)
- shared/user-util: add compat forms of user name checking functions (#1848373)
- shared/user-util: emit a warning on names with dots (#1848373)
- user-util: Allow names starting with a digit (#1848373)
- shared/user-util: allow usernames with dots in specific fields (#1848373)
- user-util: switch order of checks in valid_user_group_name_or_id_full() (#1848373)
- user-util: rework how we validate user names (#1848373)

* Wed Oct 07 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-41
- cgroup: freezer action must be NOP when cgroup v2 freezer is not available (#1868831)

* Fri Aug 28 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-40
- units: add generic boot-complete.target (#1872243)
- man: document new "boot-complete.target" unit (#1872243)
- core: make sure to restore the control command id, too (#1829867)

* Thu Aug 06 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-39
- device: make sure we emit PropertiesChanged signal once we set sysfs (#1793533)
- device: don't emit PropetiesChanged needlessly (#1793533)

* Tue Aug 04 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-38
- spec: fix rpm verification (#1702300)

* Wed Jul 08 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-37
- spec: don't package /etc/systemd/system/dbus-org.freedesktop.resolve1.service (#1844465)

* Fri Jun 26 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-36
- core: don't consider SERVICE_SKIP_CONDITION for abnormal or failure restarts (#1737283)
- selinux: do preprocessor check only in selinux-access.c (#1830861)
- basic/cgroup-util: introduce cg_get_keyed_attribute_full() (#1830861)
- shared: add generic logic for waiting for a unit to enter some state (#1830861)
- shared: fix assert call (#1830861)
- shared: Don't try calling NULL callback in bus_wait_for_units_clear (#1830861)
- shared: add NULL callback check in one more place (#1830861)
- core: introduce support for cgroup freezer (#1830861)
- core/cgroup: fix return value of unit_cgorup_freezer_action() (#1830861)
- core: fix the return value in order to make sure we don't dipatch method return too early (#1830861)
- test: add test for cgroup v2 freezer support (#1830861)
- fix mis-merge (#1848421)
- tests: sleep a bit and give kernel time to perform the action after manual freeze/thaw (#1848421)

* Fri Jun 26 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-35
- spec: fix rpm verification (#1702300)

* Thu Jun 18 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-34
- spec: fix rpm verification (#1702300)

* Tue Jun 09 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-33
- tmpfiles: fix crash with NULL in arg_root and other fixes and tests (#1836024)
- sulogin-shell: Use force if SYSTEMD_SULOGIN_FORCE set (#1625929)
- resolvconf: fixes for the compatibility interface (#1835594)
- mount: don't add Requires for tmp.mount (#1748840)
- core: coldplug possible nop_job (#1829798)
- core: add IODeviceLatencyTargetSec (#1831519)
- time-util: Introduce parse_sec_def_infinity (#1770379)
- cgroup: use structured initialization (#1770379)
- core: add CPUQuotaPeriodSec= (#1770379)
- core: downgrade CPUQuotaPeriodSec= clamping logs to debug (#1770379)
- sd-bus: avoid magic number in SASL length calculation (#1838081)
- sd-bus: fix SASL reply to empty AUTH (#1838081)
- sd-bus: skip sending formatted UIDs via SASL (#1838081)
- core: add MemoryMin (#1763435)
- core: introduce cgroup_add_device_allow() (#1763435)
- test: remove support for suffix in get_testdata_dir() (#1763435)
- cgroup: Implement default propagation of MemoryLow with DefaultMemoryLow (#1763435)
- cgroup: Create UNIT_DEFINE_ANCESTOR_MEMORY_LOOKUP (#1763435)
- unit: Add DefaultMemoryMin (#1763435)
- cgroup: Polish hierarchically aware protection docs a bit (#1763435)
- cgroup: Readd some plumbing for DefaultMemoryMin (#1763435)
- cgroup: Support 0-value for memory protection directives (#1763435)
- cgroup: Test that it's possible to set memory protection to 0 again (#1763435)
- cgroup: Check ancestor memory min for unified memory config (#1763435)
- cgroup: Respect DefaultMemoryMin when setting memory.min (#1763435)
- cgroup: Mark memory protections as explicitly set in transient units (#1763435)
- meson: allow setting the version string during configuration (#1804252)

* Thu Jun 04 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-32
- pid1: fix DefaultTasksMax initialization (#1809037)
- cgroup: make sure that cpuset is supported on cgroup v2 and disabled with v1 (#1808940)
- test: introduce TEST-36-NUMAPOLICY (#1808940)
- test: replace `tail -f` with journal cursor which should be... (#1808940)
- test: support MPOL_LOCAL matching in unpatched strace versions (#1808940)
- test: make sure the strace process is indeed dead (#1808940)
- test: skip the test on systems without NUMA support (#1808940)
- test: give strace some time to initialize (#1808940)
- test: add a simple sanity check for systems without NUMA support (#1808940)
- test: drop the missed || exit 1 expression (#1808940)
- test: replace cursor file with a plain cursor (#1808940)
- cryptsetup: Treat key file errors as a failed password attempt (#1763155)
- swap: finish the secondary swap units' jobs if deactivation of the primary swap unit fails (#1749622)
- resolved: Recover missing PrivateTmp=yes and ProtectSystem=strict (#1810869)
- bus_open leak sd_event_source when udevadm trigger。 (#1798504)
- core: rework StopWhenUnneeded= logic (#1798046)
- pid1: fix the names of AllowedCPUs= and AllowedMemoryNodes= (#1818054)
- core: fix re-realization of cgroup siblings (#1818054)
- basic: use comma as separator in cpuset cgroup cpu ranges (#1818054)
- core: transition to FINAL_SIGTERM state after ExecStopPost= (#1766479)
- sd-journal: close journal files that were deleted by journald before we've setup inotify watch (#1796128)
- sd-journal: remove the dead code and actually fix #14695 (#1796128)
- udev: downgrade message when we fail to set inotify watch up (#1808051)
- logind: check PolicyKit before allowing VT switch (#1797679)
- test: do not use global variable to pass error (#1823767)
- test: install libraries required by tests (#1823767)
- test: introduce install_zoneinfo() (#1823767)
- test: replace duplicated Makefile by symbolic link (#1823767)
- test: add paths of keymaps in install_keymaps() (#1823767)
- test: make install_keymaps() optionally install more keymaps (#1823767)
- test-fs-util: skip some tests when running in unprivileged container (#1823767)
- test-process-util: skip several verifications when running in unprivileged container (#1823767)
- test-execute: also check python3 is installed or not (#1823767)
- test-execute: skip several tests when running in container (#1823767)
- test: introduce test_is_running_from_builddir() (#1823767)
- test: make test-catalog relocatable (#1823767)
- test: parallelize tasks in TEST-24-UNIT-TESTS (#1823767)
- test: try to determine QEMU_SMP dynamically (#1823767)
- test: store coredumps in journal (#1823767)
- pid1: add new kernel cmdline arg systemd.cpu_affinity= (#1812894)
- udev-rules: make tape-changers also apprear in /dev/tape/by-path/ (#1820112)
- man: be clearer that .timer time expressions need to be reset to override them (#1816908)
- Add support for opening files for appending (#1809175)
- nspawn: move payload to sub-cgroup first, then sync cgroup trees (#1837094)
- core: move unit_status_emit_starting_stopping_reloading() and related calls to job.c (#1737283)
- job: when a job was skipped due to a failed condition, log about it (#1737283)
- core: split out all logic that updates a Job on a unit's unit_notify() invocation (#1737283)
- core: make log messages about units entering a 'failed' state recognizable (#1737283)
- core: log a recognizable message when a unit succeeds, too (#1737283)
- tests: always use the right vtable wrapper calls (#1737283)
- test-execute: allow filtering test cases by pattern (#1737283)
- test-execute: provide custom failure message (#1737283)
- core: ExecCondition= for services (#1737283)
- Drop support for lz4 < 1.3.0 (#1843871)
- test-compress: add test for short decompress_startswith calls (#1843871)
- journal: adapt for new improved LZ4_decompress_safe_partial() (#1843871)
- fuzz-compress: add fuzzer for compression and decompression (#1843871)
- seccomp: fix __NR__sysctl usage (#1843871)

* Fri Feb 21 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-27
- cgroup: introduce support for cgroup v2 CPUSET controller (#1724617)

* Wed Feb 19 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-26
- seccomp: introduce seccomp_restrict_suid_sgid() for blocking chmod() for suid/sgid files (#1687512)
- test: add test case for restrict_suid_sgid() (#1687512)
- core: expose SUID/SGID restriction as new unit setting RestrictSUIDSGID= (#1687512)
- analyze: check for RestrictSUIDSGID= in "systemd-analyze security" (#1687512)
- man: document the new RestrictSUIDSGID= setting (#1687512)
- units: turn on RestrictSUIDSGID= in most of our long-running daemons (#1687512)
- core: imply NNP and SUID/SGID restriction for DynamicUser=yes service (#1687512)

* Mon Feb 17 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-25
- sd-bus: use "queue" message references for managing r/w message queues in connection objects (CVE-2020-1712)
- pid1: make sure to restore correct default values for some rlimits (#1789930)
- main: introduce a define HIGH_RLIMIT_MEMLOCK similar to HIGH_RLIMIT_NOFILE (#1789930)

* Thu Feb 13 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-24
- rules: reintroduce 60-alias-kmsg.rules (#1739353)
- sd-bus: make rqueue/wqueue sizes of type size_t (CVE-2020-1712)
- sd-bus: reorder bus ref and bus message ref handling (CVE-2020-1712)
- sd-bus: make sure dispatch_rqueue() initializes return parameter on all types of success (CVE-2020-1712)
- sd-bus: drop two inappropriate empty lines (CVE-2020-1712)
- sd-bus: initialize mutex after we allocated the wqueue (CVE-2020-1712)
- sd-bus: always go through sd_bus_unref() to free messages (CVE-2020-1712)
- bus-message: introduce two kinds of references to bus messages (CVE-2020-1712)
- sd-bus: introduce API for re-enqueuing incoming messages (CVE-2020-1712)
- sd-event: add sd_event_source_disable_unref() helper (CVE-2020-1712)
- polkit: when authorizing via PK let's re-resolve callback/userdata instead of caching it (CVE-2020-1712)
- sysctl: let's by default increase the numeric PID range from 2^16 to 2^22 (#1744214)
- journal: do not trigger assertion when journal_file_close() get NULL (#1788085)
- journal: use cleanup attribute at one more place (#1788085)

* Mon Jan 13 2020 systemd maintenance team <systemd-maint@redhat.com> - 239-23
- catalog: fix name of variable (#1677768)
- cryptsetup: add keyfile-timeout to allow a keydev timeout and allow to fallback to a password if it fails. (#1763155)
- cryptsetup: add documentation for keyfile-timeout (#1763155)
- cryptsetup: use unabbrieviated variable names (#1763155)
- cryptsetup: don't assert on variable which is optional (#1763155)
- cryptsetup-generator: guess whether the keyfile argument is two items or one (#1763155)
- crypt-util: Translate libcryptsetup log level instead of using log_debug() (#1776408)
- cryptsetup: add some commenting about EAGAIN generation (#1776408)
- cryptsetup: downgrade a log message we ignore (#1776408)
- cryptsetup: rework how we log about activation failures (#1776408)

* Tue Dec 17 2019 systemd maintenance team <systemd-maint@redhat.com> - 239-22
- spec: don't ship /var/log/README
- spec: provide systemd-rpm-macros

* Mon Dec 09 2019 systemd maintenance team <systemd-maint@redhat.com> - 239-21
- test-cpu-set-util: fix comparison for allocation size (#1734787)
- test-cpu-set-util: fix allocation size check on i386 (#1734787)

* Mon Dec 09 2019 systemd maintenance team <systemd-maint@redhat.com> - 239-20
- journal: rely on _cleanup_free_ to free a temporary string used in client_context_read_cgroup (#1764560)
- basic/user-util: allow dots in user names (#1717603)
- sd-bus: bump message queue size again (#1770189)
- tests: put fuzz_journald_processing_function in a .c file (#1764560)
- tests: add a fuzzer for dev_kmsg_record (#1764560)
- basic: remove an assertion from cunescape_one (#1764560)
- journal: fix an off-by-one error in dev_kmsg_record (#1764560)
- tests: add a reproducer for a memory leak fixed in 30eddcd51b8a472e05d3b8d1 in August (#1764560)
- tests: add a reproducer for a heap-buffer-overflow fixed in 937b1171378bc1000a (#1764560)
- test: initialize syslog_fd in fuzz-journald-kmsg too (#1764560)
- tests: add a fuzzer for process_audit_string (#1764560)
- journald: check whether sscanf has changed the value corresponding to %n (#1764560)
- tests: introduce dummy_server_init and use it in all journald fuzzers (#1764560)
- tests: add a fuzzer for journald streams (#1764560)
- tests: add a fuzzer for server_process_native_file (#1764560)
- fuzz-journal-stream: avoid assertion failure on samples which don't fit in pipe (#1764560)
- journald: take leading spaces into account in syslog_parse_identifier (#1764560)
- Add a warning about the difference in permissions between existing directories and unit settings. (#1778384)
- execute: remove one redundant comparison check (#1778384)
- core: change ownership/mode of the execution directories also for static users (#1778384)
- core/dbus-execute: remove unnecessary initialization (#1734787)
- shared/cpu-set-util: move the part to print cpu-set into a separate function (#1734787)
- shared/cpu-set-util: remove now-unused CPU_SIZE_TO_NUM() (#1734787)
- Rework cpu affinity parsing (#1734787)
- Move cpus_in_affinity_mask() to cpu-set-util.[ch] (#1734787)
- test-cpu-set-util: add simple test for cpus_in_affinity_mask() (#1734787)
- test-cpu-set-util: add a smoke test for test_parse_cpu_set_extend() (#1734787)
- pid1: parse CPUAffinity= in incremental fashion (#1734787)
- pid1: don't reset setting from /proc/cmdline upon restart (#1734787)
- pid1: when reloading configuration, forget old settings (#1734787)
- test-execute: use CPUSet too (#1734787)
- shared/cpu-set-util: drop now-unused cleanup function (#1734787)
- shared/cpu-set-util: make transfer of cpu_set_t over bus endian safe (#1734787)
- test-cpu-set-util: add test for dbus conversions (#1734787)
- shared/cpu-set-util: introduce cpu_set_to_range() (#1734787)
- systemctl: present CPUAffinity mask as a list of CPU index ranges (#1734787)
- shared/cpu-set-util: only force range printing one time (#1734787)
- execute: dump CPUAffinity as a range string instead of a list of CPUs (#1734787)
- cpu-set-util: use %d-%d format in  cpu_set_to_range_string() only for actual ranges (#1734787)
- core: introduce NUMAPolicy and NUMAMask options (#1734787)
- core: disable CPUAccounting by default (#1734787)
- set kptr_restrict=1 (#1689346)
- cryptsetup: reduce the chance that we will be OOM killed (#1696602)
- core, job: fix breakage of ordering dependencies by systemctl reload command (#1766417)
- debug-generator: enable custom systemd.debug_shell tty (#1723722)

* Thu Oct 24 2019 Lukas Nykryn <lnykryn@redhat.com> - 239-19
- core: never propagate reload failure to service result (#1735787)
- man: document systemd-analyze security (#1750343)
- man: reorder and add examples to systemd-analyze(1) (#1750343)
- travis: move to CentOS 8 docker images (#1761519)
- travis: drop SCL remains (#1761519)
- syslog: fix segfault in syslog_parse_priority() (#1761519)
- sd-bus: make strict asan shut up (#1761519)
- travis: don't run slow tests under ASan/UBSan (#1761519)
- kernel-install: do not require non-empty kernel cmdline (#1701454)
- ask-password: prevent buffer overrow when reading from keyring (#1752050)
- core: try to reopen /dev/kmsg again right after mounting /dev (#1749212)
- buildsys: don't garbage collect sections while linking (#1748258)
- udev: introduce CONST key name (#1762679)
- Call getgroups() to know size of supplementary groups array to allocate (#1743230256 KB
#1743235)
- Consider smb3 as remote filesystem (#1757257)
- process-util: introduce pid_is_my_child() helper (#1744972)
- core: reduce the number of stalled PIDs from the watched processes list when possible (#1744972)
- core: only watch processes when it's really necessary (#1744972)
- core: implement per unit journal rate limiting (#1719577)
- path: stop watching path specs once we triggered the target unit (#1763161)
- journald: fixed assertion failure when system journal rotation fails (#9893) (#1763619)
- test: use PBKDF2 instead of Argon2 in cryptsetup... (#1761519)
- test: mask several unnecessary services (#1761519)
- test: bump the second partition's size to 50M (#1761519)
- shared/sleep-config: exclude zram devices from hibernation candidates (#1763617)
- selinux: don't log SELINUX_INFO and SELINUX_WARNING messages to audit (#1763612)
- sd-device: introduce log_device_*() macros (#1753369)
- udev: Add id program and rule for FIDO security tokens (#1753369)
- shared/but-util: drop trusted annotation from bus_open_system_watch_bind_with_description() (#1746857)
- sd-bus: adjust indentation of comments (#1746857)
- resolved: do not run loop twice (#1746857)
- resolved: allow access to Set*Link and Revert methods through polkit (#1746857)
- resolved: query polkit only after parsing the data (#1746857)

* Fri Aug 30 2019 Lukas Nykryn <lnykryn@redhat.com> - 239-18
- shared/but-util: drop trusted annotation from bus_open_system_watch_bind_with_description() (#1746857)
- sd-bus: adjust indentation of comments (#1746857)
- resolved: do not run loop twice (#1746857)
- resolved: allow access to Set*Link and Revert methods through polkit (#1746857)
- resolved: query polkit only after parsing the data (#1746857)

* Wed Aug 07 2019 Lukas Nykryn <lnykryn@redhat.com> - 239-17
- mount: simplify /proc/self/mountinfo handler (#1696178)
- mount: rescan /proc/self/mountinfo before processing waitid() results (#1696178)
- swap: scan /proc/swaps before processing waitid() results (#1696178)
- analyze-security: fix potential division by zero (#1734400)

* Fri Jul 26 2019 Lukas Nykryn <lnykryn@redhat.com> - 239-16
- sd-bus: deal with cookie overruns (#1694999)
- journal-remote: do not request Content-Length if Transfer-Encoding is chunked (#1708849)
- journal: do not remove multiple spaces after identifier in syslog message (#1691817)
- cryptsetup: Do not fallback to PLAIN mapping if LUKS data device set fails. (#1719153)
- cryptsetup: call crypt_load() for LUKS only once (#1719153)
- cryptsetup: Add LUKS2 token support. (#1719153)
- udev/scsi_id: fix incorrect page length when get device identification VPD page (#1713227)
- Change job mode of manager triggered restarts to JOB_REPLACE (#11456
#1712524)
- bash-completion: analyze: support 'security' (#1733395)
- man: note that journal does not validate syslog fields (#1707175)
- rules: skip memory hotplug on ppc64 (#1713159)

* Thu May 23 2019 Lukas Nykryn <lnykryn@redhat.com> - 239-15
- tree-wide: shorten error logging a bit (#1697893)
- nspawn: simplify machine terminate bus call (#1697893)
- nspawn: merge two variable declaration lines (#1697893)
- nspawn: rework how we allocate/kill scopes (#1697893)
- unit: enqueue cgroup empty check event if the last ref on a unit is dropped (#1697893)
- Revert "journal: remove journal audit socket" (#1699287)
- journal: don't enable systemd-journald-audit.socket by default (#1699287)
- logs-show: use grey color for de-emphasizing journal log output (#1695601)
- units: add [Install] section to tmp.mount (#1667065)
- nss: do not modify errno when NSS_STATUS_NOTFOUND or NSS_STATUS_SUCCESS (#1691691)
- util.h: add new UNPROTECT_ERRNO macro (#1691691)
- nss: unportect errno before writing to NSS' *errnop (#1691691)
- seccomp: reduce logging about failure to add syscall to seccomp (#1658691)
- format-table: when duplicating a cell, also copy the color (#1689832)
- format-table: optionally make specific cells clickable links (#1689832)
- format-table: before outputting a color, check if colors are available (#1689832)
- format-table: add option to store/format percent and uint64_t values in cells (#1689832)
- format-table: optionally allow reversing the sort order for a column (#1689832)
- format-table: add table_update() to update existing entries (#1689832)
- format-table: add an API for getting the cell at a specific row/column (#1689832)
- format-table: always underline header line (#1689832)
- format-table: add calls to query the data in a specific cell (#1689832)
- format-table: make sure we never call memcmp() with NULL parameters (#1689832)
- format-table: use right field for display (#1689832)
- format-table: add option to uppercase cells on display (#1689832)
- format-table: never try to reuse cells that have color/url/uppercase set (#1689832)
- locale-util: add logic to output smiley emojis at various happiness levels (#1689832)
- analyze: add new security verb (#1689832)
- tests: add a rudimentary fuzzer for server_process_syslog_message (#9979) (#1696224)
- journald: make it clear that dev_kmsg_record modifies the string passed to it (#1696224)
- journald: free the allocated memory before returning from dev_kmsg_record (#1696224)
- tests: rework the code fuzzing journald (#1696224)
- journald: make server_process_native_message compatible with fuzz_journald_processing_function (#1696224)
- tests: add a fuzzer for server_process_native_message (#1696224)
- tests: add a fuzzer for sd-ndisc (#1696224)
- ndisc: fix two infinite loops (#1696224)
- tests: add reproducers for several issues uncovered with fuzz-journald-syslog (#1696224)
- tests: add a reproducer for an infinite loop in ndisc_handle_datagram (#1696224)
- tests: add a reproducer for another infinite loop in ndisc_handle_datagram (#1696224)
- fuzz: rename "fuzz-corpus" directory to just "fuzz" (#1696224)
- test: add testcase for issue 10007 by oss-fuzz (#1696224)
- fuzz: unify the "fuzz-regressions" directory with the main corpus (#1696224)
- test-bus-marshal: use cescaping instead of hexmem (#1696224)
- meson: add -Dlog-trace to set LOG_TRACE (#1696224)
- meson: allow building resolved and machined without nss modules (#1696224)
- meson: drop duplicated condition (#1696224)
- meson: use .source_root() in more places (#1696224)
- meson: treat all fuzz cases as unit tests (#1696224)
- fuzz-bus-message: add fuzzer for message parsing (#1696224)
- bus-message: use structured initialization to avoid use of unitialized memory (#1696224)
- bus-message: avoid an infinite loop on empty structures (#1696224)
- bus-message: let's always use -EBADMSG when the message is bad (#1696224)
- bus-message: rename function for clarity (#1696224)
- bus-message: use define (#1696224)
- bus: do not print (null) if the message has unknown type (#1696224)
- bus-message: fix calculation of offsets table (#1696224)
- bus-message: remove duplicate assignment (#1696224)
- bus-message: fix calculation of offsets table for arrays (#1696224)
- bus-message: drop asserts in functions which are wrappers for varargs version (#1696224)
- bus-message: output debug information about offset troubles (#1696224)
- bus-message: fix skipping of array fields in !gvariant messages (#1696224)
- bus-message: also properly copy struct signature when skipping (#1696224)
- fuzz-bus-message: add two test cases that pass now (#1696224)
- bus-message: return -EBADMSG not -EINVAL on invalid !gvariant messages (#1696224)
- bus-message: avoid wrap-around when using length read from message (#1696224)
- util: do not use stack frame for parsing arbitrary inputs (#1696224)
- travis: enable ASan and UBSan on RHEL8 (#1683319)
- tests: keep SYS_PTRACE when running under ASan (#1683319)
- tree-wide: various ubsan zero size memory fixes (#1683319)
- util: introduce memcmp_safe() (#1683319)
- test-socket-util: avoid "memleak" reported by valgrind (#1683319)
- sd-journal: escape binary data in match_make_string() (#1683319)
- capability: introduce CAP_TO_MASK_CORRECTED() macro replacing CAP_TO_MASK() (#1683319)
- sd-bus: use size_t when dealing with memory offsets (#1683319)
- sd-bus: call cap_last_cap() only once in has_cap() (#1683319)
- mount-point: honour AT_SYMLINK_FOLLOW correctly (#1683319)
- travis: switch from trusty to xenial (#1683319)
- test-socket-util: Add tests for receive_fd_iov() and friends. (#1683319)
- socket-util: Introduce send_one_fd_iov() and receive_one_fd_iov() (#1683319)
- core: swap order of "n_storage_fds" and "n_socket_fds" parameters (#1683334)
- execute: use our usual syntax for defining bit masks (#1683334)
- core: introduce new Type=exec service type (#1683334)
- man: document the new Type=exec type (#1683334)
- sd-bus: allow connecting to the pseudo-container ".host" (#1683334)
- sd-login: let's also make sd-login understand ".host" (#1683334)
- test: add test for Type=exec (#1683334)
- journal-gateway: explicitly declare local variables (#1705971)
- tools: drop unused variable (#1705971)
- journal-gateway: use localStorage["cursor"] only when it has valid value (#1705971)

* Tue Apr 30 2019 Lukas Nykryn <lnykryn@redhat.com> - 239-14
- rules: implement new memory hotplug policy (#1670728)
- rules: add the rule that adds elevator= kernel command line parameter (#1670126)
- bus-socket: Fix line_begins() to accept word matching full string (#1692991)
- Refuse dbus message paths longer than BUS_PATH_SIZE_MAX limit. (#1678641)
- Allocate temporary strings to hold dbus paths on the heap (#1678641)
- sd-bus: if we receive an invalid dbus message, ignore and proceeed (#1678641)
- Revert "core: one step back again, for nspawn we actually can't wait for cgroups running empty since systemd will get exactly zero notifications about it" (#1703485)

* Tue Feb 26 2019 Lukas Nykryn <lnykryn@redhat.com> - 239-13
- rules: add the rule that adds elevator= kernel command line parameter (#1670126)

* Fri Feb 15 2019 Lukas Nykryn <lnykryn@redhat.com> - 239-12
- core: when deserializing state always use read_line(…, LONG_LINE_MAX, …) (CVE-2018-15686)
- coredump: remove duplicate MESSAGE= prefix from message (#1664976)
- journald: remove unnecessary {} (#1664976)
- journald: do not store the iovec entry for process commandline on stack (#1664976)
- basic/process-util: limit command line lengths to _SC_ARG_MAX (#1664976)
- coredump: fix message when we fail to save a journald coredump (#1664976)
- procfs-util: expose functionality to query total memory (#1664976)
- basic/prioq: add prioq_peek_item() (#1664976)
- journal: limit the number of entries in the cache based on available memory (#1664976)
- journald: periodically drop cache for all dead PIDs (#1664976)
- process-util: don't use overly large buffer to store process command line (#1664976)
- Revert "sysctl.d: switch net.ipv4.conf.all.rp_filter from 1 to 2" (#1653824)
- journal: fix syslog_parse_identifier() (#1664978)
- journald: set a limit on the number of fields (1k) (#1664977)
- journald: when processing a native message, bail more quickly on overbig messages (#1664977)
- journald: lower the maximum entry size limit to ½ for non-sealed fds (#1664977)
- µhttpd: use a cleanup function to call MHD_destroy_response (#1664977)
- journal-remote: verify entry length from header (#1664977)
- journal-remote: set a limit on the number of fields in a message (#1664977)
- journald: correctly attribute log messages also with cgroupsv1 (#1658115)
- rules: add elevator= kernel command line parameter (#1670126)

* Mon Jan 14 2019 Lukas Nykryn <lnykryn@redhat.com> - 239-11
- unit: don't add Requires for tmp.mount (#1619292)
- remove bootchart dependency (#1660119)

* Wed Dec 12 2018 Lukas Nykryn <lnykryn@redhat.com> - 239-10
- cryptsetup-generator: introduce basic keydev support (#1656869)
- cryptsetup: don't use %m if there's no error to show (#1656869)
- cryptsetup-generator: don't return error if target directory already exists (#1656869)
- cryptsetup-generator: allow whitespace characters in keydev specification (#1656869)
- rules: watch metadata changes on DASD devices (#1638676)
- sysctl.d: switch net.ipv4.conf.all.rp_filter from 1 to 2 (#1653824)

* Thu Dec 06 2018 Lukas Nykryn <lnykryn@redhat.com> - 239-9
- dissect-image: use right comparison function (#1602706)
- login: avoid leak of name returned by uid_to_name() (#1602706)
- firewall-util: add an assert that we're not overwriting a buffer (#1602706)
- journal-file: avoid calling ftruncate with invalid fd (#1602706)
- dhcp6: make sure we have enough space for the DHCP6 option header (#1643363)
- core: rename queued_message → pending_reload_message (#1647359)
- core: when we can't send the pending reload message, say we ignore it in the warning we log (#1647359)
- core: make sure we don't throttle change signal generator when a reload is pending (#1647359)
- proc-cmdline: introduce PROC_CMDLINE_RD_STRICT (#1643429)
- debug-generator: introduce rd.* version of all options (#1643429)
- chown-recursive: let's rework the recursive logic to use O_PATH (#1643368)
- chown-recursive: also drop ACLs when recursively chown()ing (#1643368)
- chown-recursive: TAKE_FD() is your friend (#1643368)
- test: add test case for recursive chown()ing (#1643368)
- Revert "sysctl.d: request ECN on both in and outgoing connections" (#1619790)
- detect-virt: do not try to read all of /proc/cpuinfo (#1631532)
- sd-bus: unify three code-paths which free struct bus_container (#1635435)
- sd-bus: properly initialize containers (#1635435)

* Tue Oct 16 2018 Lukas Nykryn <lnykryn@redhat.com> - 239-8
- revert sd-bus: unify three code-paths which free struct bus_container (#1635435)

* Fri Oct 12 2018 Michal Sekletár <msekleta@redhat.com> - 239-7
- change default cgroup hierarchy to "legacy" (#1638650)
- we never added mymachines module to passwd: or group: in RHEL8, hence don't try to remove it (#1638450)
- bump minimal size of random pool to 1024 bytes (#1619268)
- install RHEL-7 compatible rc.local (#1625209)
- backport support for sector-size crypttab option (#1572563)
- units: don't enable per-service IP firewall by default (#1630219)
- sd-bus: unify three code-paths which free struct bus_container (#1635435)
- bus-message: do not crash on message with a string of zero length (#1635439)
- bus-message: stack based buffer overflow in free_and_strdup (#1635428)
- journal: change support URL shown in the catalog entries (#1550548)

* Mon Sep 10 2018 Michal Sekletár <msekleta@redhat.com> - 239-6
- move /etc/yum/protected.d/systemd.conf to /etc/dnf/ (#1626973)

* Fri Sep 07 2018 Josh Boyer <jwboyer@redhat.com> - 239-5
- Fix file conflict between yum and systemd (#1626682)

* Tue Aug 14 2018 Michal Sekletár <msekleta@redhat.com> - 239-4
- drop the patch for delayed loading of config in net_setup_link and set NAME in prefixdevname udev rules (#1614681)
- bus: move BUS_DONT_DESTROY calls after asserts (#1610397)

* Fri Aug 10 2018 Michal Sekletár <msekleta@redhat.com> - 239-3
- net_setup_link: delay loading configuration, just before we apply it (#1614681)

* Thu Aug 09 2018 Michal Sekletár <msekleta@redhat.com> - 239-2
- 20-grubby.install: populate symvers.gz file (#1609698)
- net_setup_link: allow renaming interfaces that were renamed already
- units: drop DynamicUser=yes from systemd-resolved.service
- journal: remove journal audit socket

* Wed Aug 01 2018 Michal Sekletár <msekleta@redhat.com> - 239-1
- rebase to systemd-239
- Override systemd-user PAM config in install and not prep (patch by Filipe Brandenburger <filbranden@google.com>)
- use %%autosetup -S git_am to apply patches
- revert upstream default for RemoveIPC (#1523233)
- bump DefaultTasksMax to 80% of kernel default (#1523236)
- avoid /tmp being mounted as tmpfs without the user's will (#1578772)
- bump maximum number of processes in user slice to 80% of pid.max (#1523236)
- forwardport downstream-only udev rules from RHEL-7 (#1523227)
- don't ship systemd-networkd
- don't ship systemd-timesyncd
- add back support for WAIT_FOR to udev rules (#1523213)

* Wed May 16 2018 Jan Synáček <jsynacek@redhat.com> - 238-8
- do not mount /tmp as tmpfs (#1578772)

* Tue May 15 2018 Jan Synáček <jsynacek@redhat.com> - 238-7
- fix compilation (#1578318)

* Fri Apr 27 2018 Michal Sekletar <msekleta@redhat.com> - 238-6
- forwardport downstream-only udev rules from RHEL-7 (#1523227)
- set RemoveIPC=no by default (#1523233)

* Thu Apr 12 2018 Michal Sekletar <msekleta@redhat.com> - 238-5
- also drop qrencode-devel from BuildRequires as it is no longer needed (#1566158)

* Wed Apr 11 2018 Michal Sekletar <msekleta@redhat.com> - 238-4
- disable support for qrencode (#1566158)
- bump default journal rate limit to 10000 messages per 30s (#1563729)
- fix unit reloads (#1560549)
- don't create /var/log/journal during package installation (#1523188)

* Fri Mar 09 2018 Troy Dawson <tdawson@redhat.com> - 238-3.1
- Rebuild with cryptsetup-2

* Wed Mar  7 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-3
- Revert the patches for GRUB BootLoaderSpec support
- Add patch for /etc/machine-id creation (#1552843)

* Tue Mar  6 2018 Yu Watanabe <watanabe.yu@gmail.com> - 238-2
- Fix transfiletrigger script (#1551793)

* Mon Mar  5 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-1
- Update to latest version
- This fixes a hard-to-trigger potential vulnerability (CVE-2018-6954)
- New transfiletriggers are installed for udev hwdb and rules, the journal
  catalog, sysctl.d, binfmt.d, sysusers.d, tmpfiles.d.

* Tue Feb 27 2018 Javier Martinez Canillas <javierm@redhat.com> - 237-7.git84c8da5
- Add patch to install kernel images for GRUB BootLoaderSpec support

* Sat Feb 24 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 237-6.git84c8da5
- Create /etc/systemd in %%post libs if necessary (#1548607)

* Fri Feb 23 2018 Adam Williamson <awilliam@redhat.com> - 237-5.git84c8da5
- Use : not touch to create file in -libs %%post

* Thu Feb 22 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 237-4.git84c8da5
- Add coreutils dep for systemd-libs %%post
- Add patch to typecast USB IDs to avoid compile failure

* Wed Feb 21 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 237-3.git84c8da5
- Update some patches for test skipping that were updated upstream
  before merging
- Add /usr/lib/systemd/purge-nobody-user — a script to check if nobody is defined
  correctly and possibly replace existing mappings

* Tue Feb 20 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 237-2.gitdff4849
- Backport a bunch of patches, most notably for the journal and various
  memory issues. Some minor build fixes.
- Switch to new ldconfig macros that do nothing in F28+
- /etc/systemd/dont-synthesize-nobody is created in %%post if nfsnobody
  or nobody users are defined (#1537262)

* Fri Feb  9 2018 Zbigniew Jędrzejeweski-Szmek <zbyszek@in.waw.pl> - 237-1.git78bd769
- Update to first stable snapshot (various minor memory leaks and misaccesses,
  some documentation bugs, build fixes).

* Sun Jan 28 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 237-1
- Update to latest version

* Sun Jan 21 2018 Björn Esser <besser82@fedoraproject.org> - 236-4.git3e14c4c
- Add patch to include <crypt.h> if needed

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 236-3.git3e14c4c
- Rebuilt for switch to libxcrypt

* Thu Jan 11 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 236-2.git23e14c4
- Backport a bunch of bugfixes from upstream (#1531502, #1531381, #1526621
  various memory corruptions in systemd-networkd)
- /dev/kvm is marked as a static node which fixes permissions on s390x
  and ppc64 (#1532382)

* Fri Dec 15 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 236-1
- Update to latest version

* Mon Dec 11 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-5.git4a0e928
- Update to latest git snapshot, do not build for realz
- Switch to libidn2 again (#1449145)

* Tue Nov 07 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-4
- Rebuild for cryptsetup-2.0.0-0.2.fc28

* Wed Oct 25 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-3
- Backport a bunch of patches, including LP#172535

* Wed Oct 18 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-2
- Patches for cryptsetup _netdev

* Fri Oct  6 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-1
- Update to latest version

* Tue Sep 26 2017 Nathaniel McCallum <npmccallum@redhat.com> - 234-8
- Backport /etc/crypttab _netdev feature from upstream

* Thu Sep 21 2017 Michal Sekletar <msekleta@redhat.com> - 234-7
- Make sure to remove all device units sharing the same sysfs path (#1475570)

* Mon Sep 18 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-6
- Bump xslt recursion limit for libxslt-1.30

* Mon Jul 31 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-5
- Backport more patches (#1476005, hopefully #1462378)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-3
- Fix x-systemd.timeout=0 in /etc/fstab (#1462378)
- Minor patches (memleaks, --help fixes, seccomp on arm64)

* Thu Jul 13 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-2
- Create kvm group (#1431876)

* Thu Jul 13 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-1
- Latest release

* Sat Jul  1 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-7.git74d8f1c
- Update to snapshot
- Build with meson again

* Tue Jun 27 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-6
- Fix an out-of-bounds write in systemd-resolved (CVE-2017-9445)

* Fri Jun 16 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-5.gitec36d05
- Update to snapshot version, build with meson

* Thu Jun 15 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-4
- Backport a bunch of small fixes (memleaks, wrong format strings,
  man page clarifications, shell completion)
- Fix systemd-resolved crash on crafted DNS packet (CVE-2017-9217, #1455493)
- Fix systemd-vconsole-setup.service error on systems with no VGA console (#1272686)
- Drop soft-static uid for systemd-journal-gateway
- Use ID from /etc/os-release as ntpvendor

* Thu Mar 16 2017 Michal Sekletar <msekleta@redhat.com> - 233-3
- Backport bugfixes from upstream
- Don't return error when machinectl couldn't figure out container IP addresses (#1419501)

* Thu Mar  2 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-2
- Fix installation conflict with polkit

* Thu Mar  2 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-1
- New upstream release (#1416201, #1405439, #1420753, many others)
- New systemd-tests subpackage with "installed tests"

* Thu Feb 16 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-15
- Add %%ghost %%dir entries for .wants dirs of our targets (#1422894)

* Tue Feb 14 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-14
- Ignore the hwdb parser test

* Tue Feb 14 2017 Jan Synáček <jsynacek@redhat.com> - 232-14
- machinectl fails when virtual machine is running (#1419501)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 232-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-12
- Backport patch for initrd-switch-root.service getting killed (#1414904)
- Fix sd-journal-gatewayd -D, --trust, and COREDUMP_CONTAINER_CMDLINE
  extraction by sd-coredump.

* Sun Jan 29 2017 zbyszek <zbyszek@in.waw.pl> - 232-11
- Backport a number of patches (#1411299, #1413075, #1415745,
                                ##1415358, #1416588, #1408884)
- Fix various memleaks and unitialized variable access
- Shell completion enhancements
- Enable TPM logging by default (#1411156)
- Update hwdb (#1270124)

* Thu Jan 19 2017 Adam Williamson <awilliam@redhat.com> - 232-10
- Backport fix for boot failure in initrd-switch-root (#1414904)

* Wed Jan 18 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-9
- Add fake dependency on systemd-pam to systemd-devel to ensure systemd-pam
  is available as multilib (#1414153)

* Tue Jan 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-8
- Fix buildsystem to check for lz4 correctly (#1404406)

* Wed Jan 11 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-7
- Various small tweaks to scriplets

* Sat Jan 07 2017 Kevin Fenzi <kevin@scrye.com> - 232-6
- Fix scriptlets to never fail in libs post

* Fri Jan 06 2017 Kevin Fenzi <kevin@scrye.com> - 232-5
- Add patch from Michal Schmidt to avoid process substitution (#1392236)

* Sun Nov  6 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-4
- Rebuild (#1392236)

* Fri Nov  4 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-3
- Make /etc/dbus-1/system.d directory non-%%ghost

* Fri Nov  4 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-2
- Fix kernel-install (#1391829)
- Restore previous systemd-user PAM config (#1391836)
- Move journal-upload.conf.5 from systemd main to journal-remote subpackage (#1391833)
- Fix permissions on /var/lib/systemd/journal-upload (#1262665)

* Thu Nov  3 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-1
- Update to latest version (#998615, #1181922, #1374371, #1390704, #1384150, #1287161)
- Add %%{_isa} to Provides on arch-full packages (#1387912)
- Create systemd-coredump user in %%pre (#1309574)
- Replace grubby patch with a short-circuiting install.d "plugin"
- Enable nss-systemd in the passwd, group lines in nsswith.conf
- Add [!UNAVAIL=return] fallback after nss-resolve in hosts line in nsswith.conf
- Move systemd-nspawn man pages to the right subpackage (#1391703)

* Tue Oct 18 2016 Jan Synáček <jsynacek@redhat.com> - 231-11
- SPC - Cannot restart host operating from container (#1384523)

* Sun Oct  9 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-10
- Do not recreate /var/log/journal on upgrades (#1383066)
- Move nss-myhostname provides to systemd-libs (#1383271)

* Fri Oct  7 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-9
- Fix systemctl set-default (#1374371)
- Prevent systemd-udev-trigger.service from restarting (follow-up for #1378974)

* Tue Oct  4 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-8
- Apply fix for #1378974

* Mon Oct  3 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-7
- Apply patches properly

* Thu Sep 29 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-6
- Better fix for (#1380286)

* Thu Sep 29 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-5
- Denial-of-service bug against pid1 (#1380286)

* Thu Aug 25 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-4
- Fix preset-all (#1363858)
- Fix issue with daemon-reload messing up graphics (#1367766)
- A few other bugfixes

* Wed Aug 03 2016 Adam Williamson <awilliam@redhat.com> - 231-3
- Revert preset-all change, it broke stuff (#1363858)

* Wed Jul 27 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 231-2
- Call preset-all on initial installation (#1118740)
- Fix botched Recommends for libxkbcommon

* Tue Jul 26 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 231-1
- Update to latest version

* Wed Jun  8 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 230-3
- Update to latest git snapshot (fixes for systemctl set-default,
  polkit lingering policy, reversal of the framebuffer rules,
  unaligned access fixes, fix for StartupBlockIOWeight-over-dbus).
  Those changes are interspersed with other changes and new features
  (mostly in lldp, networkd, and nspawn). Some of those new features
  might not work, but I think that existing functionality should not
  be broken, so it seems worthwile to update to the snapshot.

* Sat May 21 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 230-2
- Remove systemd-compat-libs on upgrade

* Sat May 21 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 230-1
- New version
- Drop compat-libs
- Require libxkbcommon explictly, since the automatic dependency will
  not be generated anymore

* Tue Apr 26 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 229-15
- Remove duplicated entries in -container %%files (#1330395)

* Fri Apr 22 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-14
- Move installation of udev services to udev subpackage (#1329023)

* Mon Apr 18 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-13
- Split out systemd-pam subpackage (#1327402)

* Mon Apr 18 2016 Harald Hoyer <harald@redhat.com> - 229-12
- move more binaries and services from the main package to subpackages

* Mon Apr 18 2016 Harald Hoyer <harald@redhat.com> - 229-11
- move more binaries and services from the main package to subpackages

* Mon Apr 18 2016 Harald Hoyer <harald@redhat.com> - 229-10
- move device dependant stuff to the udev subpackage

* Tue Mar 22 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-9
- Add myhostname to /etc/nsswitch.conf (#1318303)

* Mon Mar 21 2016 Harald Hoyer <harald@redhat.com> - 229-8
- fixed kernel-install for copying files for grubby
Resolves:             rhbz#1299019

* Thu Mar 17 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-7
- Moar patches (#1316964, #1317928)
- Move vconsole-setup and tmpfiles-setup-dev bits to systemd-udev
- Protect systemd-udev from deinstallation

* Fri Mar 11 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-6
- Create /etc/resolv.conf symlink from systemd-resolved (#1313085)

* Fri Mar  4 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-5
- Split out systemd-container subpackage (#1163412)
- Split out system-udev subpackage
- Add various bugfix patches, incl. a tentative fix for #1308771

* Tue Mar  1 2016 Peter Robinson <pbrobinson@fedoraproject.org> 229-4
- Power64 and s390(x) now have libseccomp support
- aarch64 has gnu-efi

* Tue Feb 23 2016 Jan Synáček <jsynacek@redhat.com> - 229-3
- Fix build failures on ppc64 (#1310800)

* Tue Feb 16 2016 Dennis Gilmore <dennis@ausil.us> - 229-2
- revert: fixed kernel-install for copying files for grubby
Resolves:             rhbz#1299019
- this causes the dtb files to not get installed at all and the fdtdir
- line in extlinux.conf to not get updated correctly

* Thu Feb 11 2016 Michal Sekletar <msekleta@redhat.com> - 229-1
- New upstream release

* Thu Feb 11 2016 Harald Hoyer <harald@redhat.com> - 228-10.gite35a787
- fixed kernel-install for copying files for grubby
Resolves:             rhbz#1299019

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 228-9.gite35a787
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Peter Robinson <pbrobinson@fedoraproject.org> 228-8.gite35a787
- Rebuild for binutils on aarch64 fix

* Fri Jan 08 2016 Dan Horák <dan[at]danny.cz> - 228-7.gite35a787
- apply the conflict with fedora-release only in Fedora

* Thu Dec 10 2015 Jan Synáček <jsynacek@redhat.com> - 228-6.gite35a787
- Fix rawhide build failures on ppc64 (#1286249)

* Sun Nov 29 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-6.gite35a787
- Create /etc/systemd/network (#1286397)

* Thu Nov 26 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-5.gite35a787
- Do not install nss modules by default

* Tue Nov 24 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-4.gite35a787
- Update to latest upstream git: there is a bunch of fixes
  (nss-mymachines overflow bug, networkd fixes, more completions are
  properly installed), mixed with some new resolved features.
- Rework file triggers so that they always run before daemons are restarted

* Thu Nov 19 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-3
- Enable rpm file triggers for daemon-reload

* Thu Nov 19 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-2
- Fix version number in obsoleted package name (#1283452)

* Wed Nov 18 2015 Kay Sievers <kay@redhat.com> - 228-1
- New upstream release

* Thu Nov 12 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 227-7
- Rename journal-gateway subpackage to journal-remote
- Ignore the access mode on /var/log/journal (#1048424)
- Do not assume fstab is present (#1281606)

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 227-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov 10 2015 Lukáš Nykrýn <lnykryn@redhat.com> - 227-5
- Rebuild for libmicrohttpd soname bump

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 227-4
- Rebuilt for Python3.5 rebuild

* Wed Nov  4 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 227-3
- Fix syntax in kernel-install (#1277264)

* Tue Nov 03 2015 Michal Schmidt <mschmidt@redhat.com> - 227-2
- Rebuild for libmicrohttpd soname bump.

* Wed Oct  7 2015 Kay Sievers <kay@redhat.com> - 227-1
- New upstream release

* Fri Sep 18 2015 Jan Synáček <jsynacek@redhat.com> - 226-3
- user systemd-journal-upload should be in systemd-journal group (#1262743)

* Fri Sep 18 2015 Kay Sievers <kay@redhat.com> - 226-2
- Add selinux to  system-user PAM config

* Tue Sep  8 2015 Kay Sievers <kay@redhat.com> - 226-1
- New upstream release

* Thu Aug 27 2015 Kay Sievers <kay@redhat.com> - 225-1
- New upstream release

* Fri Jul 31 2015 Kay Sievers <kay@redhat.com> - 224-1
- New upstream release

* Wed Jul 29 2015 Kay Sievers <kay@redhat.com> - 223-2
- update to git snapshot

* Wed Jul 29 2015 Kay Sievers <kay@redhat.com> - 223-1
- New upstream release

* Thu Jul  9 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 222-2
- Remove python subpackages (python-systemd in now standalone)

* Tue Jul  7 2015 Kay Sievers <kay@redhat.com> - 222-1
- New upstream release

* Mon Jul  6 2015 Kay Sievers <kay@redhat.com> - 221-5.git619b80a
- update to git snapshot

* Mon Jul  6 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@laptop> - 221-4.git604f02a
- Add example file with yama config (#1234951)

* Sun Jul 5 2015 Kay Sievers <kay@redhat.com> - 221-3.git604f02a
- update to git snapshot

* Mon Jun 22 2015 Kay Sievers <kay@redhat.com> - 221-2
- build systemd-boot EFI tools

* Fri Jun 19 2015 Lennart Poettering <lpoetter@redhat.com> - 221-1
- New upstream release
- Undoes botched translation check, should be reinstated later?

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 220-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Peter Robinson <pbrobinson@fedoraproject.org> 220-9
- The gold linker is now fixed on aarch64

* Tue Jun  9 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 220-8
- Remove gudev which is now provided as separate package (libgudev)
- Fix for spurious selinux denials (#1224211)
- Udev change events (#1225905)
- Patches for some potential crashes
- ProtectSystem=yes does not touch /home
- Man page fixes, hwdb updates, shell completion updates
- Restored persistent device symlinks for bcache, xen block devices
- Tag all DRM cards as master-of-seat

* Tue Jun 09 2015 Harald Hoyer <harald@redhat.com> 220-7
- fix udev block device watch

* Tue Jun 09 2015 Harald Hoyer <harald@redhat.com> 220-6
- add support for network disk encryption

* Sun Jun  7 2015 Peter Robinson <pbrobinson@fedoraproject.org> 220-5
- Disable gold on aarch64 until it's fixed (tracked in rhbz #1225156)

* Sat May 30 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 220-4
- systemd-devel should require systemd-libs, not the main package (#1226301)
- Check for botched translations (#1226566)
- Make /etc/udev/hwdb.d part of the rpm (#1226379)

* Thu May 28 2015 Richard W.M. Jones <rjones@redhat.com> - 220-3
- Add patch to fix udev --daemon not cleaning child processes
  (upstream commit 86c3bece38bcf5).

* Wed May 27 2015 Richard W.M. Jones <rjones@redhat.com> - 220-2
- Add patch to fix udev --daemon crash (upstream commit 040e689654ef08).

* Thu May 21 2015 Lennart Poettering <lpoetter@redhat.com> - 220-1
- New upstream release
- Drop /etc/mtab hack, as that's apparently fixed in mock now (#1116158)
- Remove ghosting for %%{_sysconfdir}/systemd/system/runlevel*.target, these targets are not configurable anymore in systemd upstream
- Drop work-around for #1002806, since this is solved upstream now

* Wed May 20 2015 Dennis Gilmore <dennis@ausil.us> - 219-15
- fix up the conflicts version for fedora-release

* Wed May 20 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-14
- Remove presets (#1221340)
- Fix (potential) crash and memory leak in timedated, locking failure
  in systemd-nspawn, crash in resolved.
- journalctl --list-boots should be faster
- zsh completions are improved
- various ommissions in docs are corrected (#1147651)
- VARIANT and VARIANT_ID fields in os-release are documented
- systemd-fsck-root.service is generated in the initramfs (#1201979, #1107818)
- systemd-tmpfiles should behave better on read-only file systems (#1207083)

* Wed Apr 29 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-13
- Patches for some outstanding annoyances
- Small keyboard hwdb updates

* Wed Apr  8 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-12
- Tighten requirements between subpackages (#1207381).

* Sun Mar 22 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-11
- Move all parts systemd-journal-{remote,upload} to
  systemd-journal-gatewayd subpackage (#1193143).
- Create /var/lib/systemd/journal-upload directory (#1193145).
- Cut out lots of stupid messages at debug level which were obscuring more
  important stuff.
- Apply "tentative" state for devices only when they are added, not removed.
- Ignore invalid swap pri= settings (#1204336)
- Fix SELinux check for timedated operations to enable/disable ntp (#1014315)
- Fix comparing of filesystem paths (#1184016)

* Sat Mar 14 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-10
- Fixes for bugs 1186018, 1195294, 1185604, 1196452.
- Hardware database update.
- Documentation fixes.
- A fix for journalctl performance regression.
- Fix detection of inability to open files in journalctl.
- Detect SuperH architecture properly.
- The first of duplicate lines in tmpfiles wins again.
- Do vconsole setup after loading vconsole driver, not fbcon.
- Fix problem where some units were restarted during systemd reexec.
- Fix race in udevadm settle tripping up NetworkManager.
- Downgrade various log messages.
- Fix issue where journal-remote would process some messages with a delay.
- GPT /srv partition autodiscovery is fixed.
- Reconfigure old Finnish keymaps in post (#1151958)

* Tue Mar 10 2015 Jan Synáček <jsynacek@redhat.com> - 219-9
- Buttons on Lenovo X6* tablets broken (#1198939)

* Tue Mar  3 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-8
- Reworked device handling (#1195761)
- ACL handling fixes (with a script in %%post)
- Various log messages downgraded (#1184712)
- Allow PIE on s390 again (#1197721)

* Wed Feb 25 2015 Michal Schmidt <mschmidt@redhat.com> - 219-7
- arm: reenable lto. gcc-5.0.0-0.16 fixed the crash (#1193212)

* Tue Feb 24 2015 Colin Walters <walters@redhat.com> - 219-6
- Revert patch that breaks Atomic/OSTree (#1195761)

* Fri Feb 20 2015 Michal Schmidt <mschmidt@redhat.com> - 219-5
- Undo the resolv.conf workaround, Aim for a proper fix in Rawhide.

* Fri Feb 20 2015 Michal Schmidt <mschmidt@redhat.com> - 219-4
- Revive fedora-disable-resolv.conf-symlink.patch to unbreak composes.

* Wed Feb 18 2015 Michal Schmidt <mschmidt@redhat.com> - 219-3
- arm: disabling gold did not help; disable lto instead (#1193212)

* Tue Feb 17 2015 Peter Jones <pjones@redhat.com> - 219-2
- Update 90-default.present for dbxtool.

* Mon Feb 16 2015 Lennart Poettering <lpoetter@redhat.com> - 219-1
- New upstream release
- This removes the sysctl/bridge hack, a different solution needs to be found for this (see #634736)
- This removes the /etc/resolv.conf hack, anaconda needs to fix their handling of /etc/resolv.conf as symlink
- This enables "%%check"
- disable gold on arm, as that is broken (see #1193212)

* Mon Feb 16 2015 Peter Robinson <pbrobinson@fedoraproject.org> 218-6
- aarch64 now has seccomp support

* Thu Feb 05 2015 Michal Schmidt <mschmidt@redhat.com> - 218-5
- Don't overwrite systemd.macros with unrelated Source file.

* Thu Feb  5 2015 Jan Synáček <jsynacek@redhat.com> - 218-4
- Add a touchpad hwdb (#1189319)

* Thu Jan 15 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 218-4
- Enable xkbcommon dependency to allow checking of keymaps
- Fix permissions of /var/log/journal (#1048424)
- Enable timedatex in presets (#1187072)
- Disable rpcbind in presets (#1099595)

* Wed Jan  7 2015 Jan Synáček <jsynacek@redhat.com> - 218-3
- RFE: journal: automatically rotate the file if it is unlinked (#1171719)

* Mon Jan 05 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 218-3
- Add firewall description files (#1176626)

* Thu Dec 18 2014 Jan Synáček <jsynacek@redhat.com> - 218-2
- systemd-nspawn doesn't work on s390/s390x (#1175394)

* Wed Dec 10 2014 Lennart Poettering <lpoetter@redhat.com> - 218-1
- New upstream release
- Enable "nss-mymachines" in /etc/nsswitch.conf

* Thu Nov 06 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 217-4
- Change libgudev1 to only require systemd-libs (#727499), there's
  no need to require full systemd stack.
- Fixes for bugs #1159448, #1152220, #1158035.
- Bash completions updates to allow propose more units for start/restart,
  and completions for set-default,get-default.
- Again allow systemctl enable of instances.
- Hardware database update and fixes.
- Udev crash on invalid options and kernel commandline timeout parsing are fixed.
- Add "embedded" chassis type.
- Sync before 'reboot -f'.
- Fix restarting of timer units.

* Wed Nov 05 2014 Michal Schmidt <mschmidt@redhat.com> - 217-3
- Fix hanging journal flush (#1159641)

* Fri Oct 31 2014 Michal Schmidt <mschmidt@redhat.com> - 217-2
- Fix ordering cycles involving systemd-journal-flush.service and
  remote-fs.target (#1159117)

* Tue Oct 28 2014 Lennart Poettering <lpoetter@redhat.com> - 217-1
- New upstream release

* Fri Oct 17 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-12
- Drop PackageKit.service from presets (#1154126)

* Mon Oct 13 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-11
- Conflict with old versions of initscripts (#1152183)
- Remove obsolete Finnish keymap (#1151958)

* Fri Oct 10 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-10
- Fix a problem with voluntary daemon exits and some other bugs
  (#1150477, #1095962, #1150289)

* Fri Oct 03 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-9
- Update to latest git, but without the readahead removal patch
  (#1114786, #634736)

* Wed Oct 01 2014 Kay Sievers <kay@redhat.com> - 216-8
- revert "don't reset selinux context during CHANGE events"

* Wed Oct 01 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 216-7
- add temporary workaround for #1147910
- don't reset selinux context during CHANGE events

* Wed Sep 10 2014 Michal Schmidt <mschmidt@redhat.com> - 216-6
- Update timesyncd with patches to avoid hitting NTP pool too often.

* Tue Sep 09 2014 Michal Schmidt <mschmidt@redhat.com> - 216-5
- Use common CONFIGURE_OPTS for build2 and build3.
- Configure timesyncd with NTP servers from Fedora/RHEL vendor zone.

* Wed Sep 03 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-4
- Move config files for sd-j-remote/upload to sd-journal-gateway subpackage (#1136580)

* Thu Aug 28 2014 Peter Robinson <pbrobinson@fedoraproject.org> 216-3
- Drop no LTO build option for aarch64/s390 now it's fixed in binutils (RHBZ 1091611)

* Thu Aug 21 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-2
- Re-add patch to disable resolve.conf symlink (#1043119)

* Wed Aug 20 2014 Lennart Poettering <lpoetter@redhat.com> - 216-1
- New upstream release

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 215-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Dan Horák <dan[at]danny.cz> 215-11
- disable LTO also on s390(x)

* Sat Aug 09 2014 Harald Hoyer <harald@redhat.com> 215-10
- fixed PPC64LE

* Wed Aug  6 2014 Tom Callaway <spot@fedoraproject.org> - 215-9
- fix license handling

* Wed Jul 30 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-8
- Create systemd-journal-remote and systemd-journal-upload users (#1118907)

* Thu Jul 24 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-7
- Split out systemd-compat-libs subpackage

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 215-6
- Rebuilt for gobject-introspection 1.41.4

* Mon Jul 21 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-5
- Fix SELinux context of /etc/passwd-, /etc/group-, /etc/.updated (#1121806)
- Add missing BR so gnutls and elfutils are used

* Sat Jul 19 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-4
- Various man page updates
- Static device node logic is conditionalized on CAP_SYS_MODULES instead of CAP_MKNOD
  for better behaviour in containers
- Some small networkd link handling fixes
- vconsole-setup runs setfont before loadkeys (https://bugs.freedesktop.org/show_bug.cgi?id=80685)
- New systemd-escape tool
- XZ compression settings are tweaked to greatly improve journald performance
- "watch" is accepted as chassis type
- Various sysusers fixes, most importantly correct selinux labels
- systemd-timesyncd bug fix (https://bugs.freedesktop.org/show_bug.cgi?id=80932)
- Shell completion improvements
- New udev tag ID_SOFTWARE_RADIO can be used to instruct logind to allow user access
- XEN and s390 virtualization is properly detected

* Mon Jul 07 2014 Colin Walters <walters@redhat.com> - 215-3
- Add patch to disable resolve.conf symlink (#1043119)

* Sun Jul 06 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-2
- Move systemd-journal-remote to systemd-journal-gateway package (#1114688)
- Disable /etc/mtab handling temporarily (#1116158)

* Thu Jul 03 2014 Lennart Poettering <lpoetter@redhat.com> - 215-1
- New upstream release
- Enable coredump logic (which abrt would normally override)

* Sun Jun 29 2014 Peter Robinson <pbrobinson@fedoraproject.org> 214-5
- On aarch64 disable LTO as it still has issues on that arch

* Thu Jun 26 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 214-4
- Bugfixes (#996133, #1112908)

* Mon Jun 23 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 214-3
- Actually create input group (#1054549)

* Sun Jun 22 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 214-2
- Do not restart systemd-logind on upgrades (#1110697)
- Add some patches (#1081429, #1054549, #1108568, #928962)

* Wed Jun 11 2014 Lennart Poettering <lpoetter@redhat.com> - 214-1
- New upstream release
- Get rid of "floppy" group, since udev uses "disk" now
- Reenable LTO

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 213-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kay Sievers <kay@redhat.com> - 213-3
- fix systemd-timesync user creation

* Wed May 28 2014 Michal Sekletar <msekleta@redhat.com> - 213-2
- Create temporary files after installation (#1101983)
- Add sysstat-collect.timer, sysstat-summary.timer to preset policy (#1101621)

* Wed May 28 2014 Kay Sievers <kay@redhat.com> - 213-1
- New upstream release

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 212-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri May 23 2014 Adam Williamson <awilliam@redhat.com> - 212-5
- revert change from 212-4, causes boot fail on single CPU boxes (RHBZ 1095891)

* Wed May 07 2014 Kay Sievers <kay@redhat.com> - 212-4
- add netns udev workaround

* Wed May 07 2014 Michal Sekletar <msekleta@redhat.com> - 212-3
- enable uuidd.socket by default (#1095353)

* Sat Apr 26 2014 Peter Robinson <pbrobinson@fedoraproject.org> 212-2
- Disable building with -flto for the moment due to gcc 4.9 issues (RHBZ 1091611)

* Tue Mar 25 2014 Lennart Poettering <lpoetter@redhat.com> - 212-1
- New upstream release

* Mon Mar 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> 211-2
- Explicitly define which upstream platforms support libseccomp

* Tue Mar 11 2014 Lennart Poettering <lpoetter@redhat.com> - 211-1
- New upstream release

* Mon Mar 10 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-8
- Fix logind unpriviledged reboot issue and a few other minor fixes
- Limit generator execution time
- Recognize buttonless joystick types

* Fri Mar 07 2014 Karsten Hopp <karsten@redhat.com> 210-7
- ppc64le needs link warnings disabled, too

* Fri Mar 07 2014 Karsten Hopp <karsten@redhat.com> 210-6
- move ifarch ppc64le to correct place (libseccomp req)

* Fri Mar 07 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-5
- Bugfixes: #1047568, #1047039, #1071128, #1073402
- Bash completions for more systemd tools
- Bluetooth database update
- Manpage fixes

* Thu Mar 06 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-4
- Apply work-around for ppc64le too (#1073647).

* Sat Mar 01 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-3
- Backport a few patches, add completion for systemd-nspawn.

* Fri Feb 28 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-3
- Apply work-arounds for ppc/ppc64 for bugs 1071278 and 1071284

* Mon Feb 24 2014 Lennart Poettering <lpoetter@redhat.com> - 210-2
- Check more services against preset list and enable by default

* Mon Feb 24 2014 Lennart Poettering <lpoetter@redhat.com> - 210-1
- new upstream release

* Sun Feb 23 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 209-2.gitf01de96
- Enable dnssec-triggerd.service by default (#1060754)

* Sun Feb 23 2014 Kay Sievers <kay@redhat.com> - 209-2.gitf01de96
- git snapshot to sort out ARM build issues

* Thu Feb 20 2014 Lennart Poettering <lpoetter@redhat.com> - 209-1
- new upstream release

* Tue Feb 18 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-15
- Make gpsd lazily activated (#1066421)

* Mon Feb 17 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-14
- Back out patch which causes user manager to be destroyed when unneeded
  and spams logs (#1053315)

* Sun Feb 16 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-13
- A different fix for #1023820 taken from Mageia
- Backported fix for #997031
- Hardward database updates, man pages improvements, a few small memory
  leaks, utf-8 correctness and completion fixes
- Support for key-slot option in crypttab

* Sat Jan 25 2014 Ville Skyttä <ville.skytta@iki.fi> - 208-12
- Own the %%{_prefix}/lib/kernel(/*) and %%{_datadir}/zsh(/*) dirs.

* Tue Dec 03 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-11
- Backport a few fixes, relevant documentation updates, and HWDB changes
  (#1051797, #1051768, #1047335, #1047304, #1047186, #1045849, #1043304,
   #1043212, #1039351, #1031325, #1023820, #1017509, #953077)
- Flip journalctl to --full by default (#984758)

* Tue Dec 03 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-9
- Apply two patches for #1026860

* Tue Dec 03 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-8
- Bump release to stay ahead of f20

* Tue Dec 03 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-7
- Backport patches (#1023041, #1036845, #1006386?)
- HWDB update
- Some small new features: nspawn --drop-capability=, running PID 1 under
  valgrind, "yearly" and "annually" in calendar specifications
- Some small documentation and logging updates

* Tue Nov 19 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-6
- Bump release to stay ahead of f20

* Tue Nov 19 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-5
- Use unit name in PrivateTmp= directories (#957439)
- Update manual pages, completion scripts, and hardware database
- Configurable Timeouts/Restarts default values
- Support printing of timestamps on the console
- Fix some corner cases in detecting when writing to the console is safe
- Python API: convert keyword values to string, fix sd_is_booted() wrapper
- Do not tread missing /sbin/fsck.btrfs as an error (#1015467)
- Allow masking of fsck units
- Advertise hibernation to swap files
- Fix SO_REUSEPORT settings
- Prefer converted xkb keymaps to legacy keymaps (#981805, #1026872)
- Make use of newer kmod
- Assorted bugfixes: #1017161, #967521, #988883, #1027478, #821723, #1014303

* Tue Oct 22 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-4
- Add temporary fix for #1002806

* Mon Oct 21 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-3
- Backport a bunch of fixes and hwdb updates

* Wed Oct 2 2013 Lennart Poettering <lpoetter@redhat.com> - 208-2
- Move old random seed and backlight files into the right place

* Wed Oct 2 2013 Lennart Poettering <lpoetter@redhat.com> - 208-1
- New upstream release

* Thu Sep 26 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> 207-5
- Do not create /var/var/... dirs

* Wed Sep 18 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> 207-4
- Fix policykit authentication
- Resolves: rhbz#1006680

* Tue Sep 17 2013 Harald Hoyer <harald@redhat.com> 207-3
- fixed login
- Resolves: rhbz#1005233

* Mon Sep 16 2013 Harald Hoyer <harald@redhat.com> 207-2
- add some upstream fixes for 207
- fixed swap activation
- Resolves: rhbz#1008604

* Fri Sep 13 2013 Lennart Poettering <lpoetter@redhat.com> - 207-1
- New upstream release

* Fri Sep 06 2013 Harald Hoyer <harald@redhat.com> 206-11
- support "debug" kernel command line parameter
- journald: fix fd leak in journal_file_empty
- journald: fix vacuuming of archived journals
- libudev: enumerate - do not try to match against an empty subsystem
- cgtop: fixup the online help
- libudev: fix memleak when enumerating childs

* Wed Sep 04 2013 Harald Hoyer <harald@redhat.com> 206-10
- Do not require grubby, lorax now takes care of grubby
- cherry-picked a lot of patches from upstream

* Tue Aug 27 2013 Dennis Gilmore <dennis@ausil.us> - 206-9
- Require grubby, Fedora installs require grubby,
- kernel-install took over from new-kernel-pkg
- without the Requires we are unable to compose Fedora
- everyone else says that since kernel-install took over
- it is responsible for ensuring that grubby is in place
- this is really what we want for Fedora

* Tue Aug 27 2013 Kay Sievers <kay@redhat.com> - 206-8
- Revert "Require grubby its needed by kernel-install"

* Mon Aug 26 2013 Dennis Gilmore <dennis@ausil.us> 206-7
- Require grubby its needed by kernel-install

* Thu Aug 22 2013 Harald Hoyer <harald@redhat.com> 206-6
- kernel-install now understands kernel flavors like PAE

* Tue Aug 20 2013 Rex Dieter <rdieter@fedoraproject.org> - 206-5
- add sddm.service to preset file (#998978)

* Fri Aug 16 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 206-4
- Filter out provides for private python modules.
- Add requires on kmod >= 14 (#990994).

* Sun Aug 11 2013 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - 206-3
- New systemd-python3 package (#976427).
- Add ownership of a few directories that we create (#894202).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 206-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Kay Sievers <kay@redhat.com> - 206-1
- New upstream release
  Resolves (#984152)

* Wed Jul  3 2013 Lennart Poettering <lpoetter@redhat.com> - 205-1
- New upstream release

* Wed Jun 26 2013 Michal Schmidt <mschmidt@redhat.com> 204-10
- Split systemd-journal-gateway subpackage (#908081).

* Mon Jun 24 2013 Michal Schmidt <mschmidt@redhat.com> 204-9
- Rename nm_dispatcher to NetworkManager-dispatcher in default preset (#977433)

* Fri Jun 14 2013 Harald Hoyer <harald@redhat.com> 204-8
- fix, which helps to sucessfully browse journals with
  duplicated seqnums

* Fri Jun 14 2013 Harald Hoyer <harald@redhat.com> 204-7
- fix duplicate message ID bug
Resolves:             rhbz#974132

* Thu Jun 06 2013 Harald Hoyer <harald@redhat.com> 204-6
- introduce 99-default-disable.preset

* Thu Jun  6 2013 Lennart Poettering <lpoetter@redhat.com> - 204-5
- Rename 90-display-manager.preset to 85-display-manager.preset so that it actually takes precedence over 90-default.preset's "disable *" line (#903690)

* Tue May 28 2013 Harald Hoyer <harald@redhat.com> 204-4
- Fix kernel-install (#965897)

* Wed May 22 2013 Kay Sievers <kay@redhat.com> - 204-3
- Fix kernel-install (#965897)

* Thu May  9 2013 Lennart Poettering <lpoetter@redhat.com> - 204-2
- New upstream release
- disable isdn by default (#959793)

* Tue May 07 2013 Harald Hoyer <harald@redhat.com> 203-2
- forward port kernel-install-grubby.patch

* Tue May  7 2013 Lennart Poettering <lpoetter@redhat.com> - 203-1
- New upstream release

* Wed Apr 24 2013 Harald Hoyer <harald@redhat.com> 202-3
- fix ENOENT for getaddrinfo
- Resolves: rhbz#954012 rhbz#956035
- crypt-setup-generator: correctly check return of strdup
- logind-dbus: initialize result variable
- prevent library underlinking

* Fri Apr 19 2013 Harald Hoyer <harald@redhat.com> 202-2
- nspawn create empty /etc/resolv.conf if necessary
- python wrapper: add sd_journal_add_conjunction()
- fix s390 booting
- Resolves: rhbz#953217

* Thu Apr 18 2013 Lennart Poettering <lpoetter@redhat.com> - 202-1
- New upstream release

* Tue Apr 09 2013 Michal Schmidt <mschmidt@redhat.com> - 201-2
- Automatically discover whether to run autoreconf and add autotools and git
  BuildRequires based on the presence of patches to be applied.
- Use find -delete.

* Mon Apr  8 2013 Lennart Poettering <lpoetter@redhat.com> - 201-1
- New upstream release

* Mon Apr  8 2013 Lennart Poettering <lpoetter@redhat.com> - 200-4
- Update preset file

* Fri Mar 29 2013 Lennart Poettering <lpoetter@redhat.com> - 200-3
- Remove NetworkManager-wait-online.service from presets file again, it should default to off

* Fri Mar 29 2013 Lennart Poettering <lpoetter@redhat.com> - 200-2
- New upstream release

* Tue Mar 26 2013 Lennart Poettering <lpoetter@redhat.com> - 199-2
- Add NetworkManager-wait-online.service to the presets file

* Tue Mar 26 2013 Lennart Poettering <lpoetter@redhat.com> - 199-1
- New upstream release

* Mon Mar 18 2013 Michal Schmidt <mschmidt@redhat.com> 198-7
- Drop /usr/s?bin/ prefixes.

* Fri Mar 15 2013 Harald Hoyer <harald@redhat.com> 198-6
- run autogen to pickup all changes

* Fri Mar 15 2013 Harald Hoyer <harald@redhat.com> 198-5
- do not mount anything, when not running as pid 1
- add initrd.target for systemd in the initrd

* Wed Mar 13 2013 Harald Hoyer <harald@redhat.com> 198-4
- fix switch-root and local-fs.target problem
- patch kernel-install to use grubby, if available

* Fri Mar 08 2013 Harald Hoyer <harald@redhat.com> 198-3
- add Conflict with dracut < 026 because of the new switch-root isolate

* Thu Mar  7 2013 Lennart Poettering <lpoetter@redhat.com> - 198-2
- Create required users

* Thu Mar 7 2013 Lennart Poettering <lpoetter@redhat.com> - 198-1
- New release
- Enable journal persistancy by default

* Sun Feb 10 2013 Peter Robinson <pbrobinson@fedoraproject.org> 197-3
- Bump for ARM

* Fri Jan 18 2013 Michal Schmidt <mschmidt@redhat.com> - 197-2
- Added qemu-guest-agent.service to presets (Lennart, #885406).
- Add missing pygobject3-base to systemd-analyze deps (Lennart).
- Do not require hwdata, it is all in the hwdb now (Kay).
- Drop dependency on dbus-python.

* Tue Jan  8 2013 Lennart Poettering <lpoetter@redhat.com> - 197-1
- New upstream release

* Mon Dec 10 2012 Michal Schmidt <mschmidt@redhat.com> - 196-4
- Enable rngd.service by default (#857765).

* Mon Dec 10 2012 Michal Schmidt <mschmidt@redhat.com> - 196-3
- Disable hardening on s390(x) because PIE is broken there and produces
  text relocations with __thread (#868839).

* Wed Dec 05 2012 Michal Schmidt <mschmidt@redhat.com> - 196-2
- added spice-vdagentd.service to presets (Lennart, #876237)
- BR cryptsetup-devel instead of the legacy cryptsetup-luks-devel provide name
  (requested by Milan Brož).
- verbose make to see the actual build flags

* Wed Nov 21 2012 Lennart Poettering <lpoetter@redhat.com> - 196-1
- New upstream release

* Tue Nov 20 2012 Lennart Poettering <lpoetter@redhat.com> - 195-8
- https://bugzilla.redhat.com/show_bug.cgi?id=873459
- https://bugzilla.redhat.com/show_bug.cgi?id=878093

* Thu Nov 15 2012 Michal Schmidt <mschmidt@redhat.com> - 195-7
- Revert udev killing cgroup patch for F18 Beta.
- https://bugzilla.redhat.com/show_bug.cgi?id=873576

* Fri Nov 09 2012 Michal Schmidt <mschmidt@redhat.com> - 195-6
- Fix cyclical dep between systemd and systemd-libs.
- Avoid broken build of test-journal-syslog.
- https://bugzilla.redhat.com/show_bug.cgi?id=873387
- https://bugzilla.redhat.com/show_bug.cgi?id=872638

* Thu Oct 25 2012 Kay Sievers <kay@redhat.com> - 195-5
- require 'sed', limit HOSTNAME= match

* Wed Oct 24 2012 Michal Schmidt <mschmidt@redhat.com> - 195-4
- add dmraid-activation.service to the default preset
- add yum protected.d fragment
- https://bugzilla.redhat.com/show_bug.cgi?id=869619
- https://bugzilla.redhat.com/show_bug.cgi?id=869717

* Wed Oct 24 2012 Kay Sievers <kay@redhat.com> - 195-3
- Migrate /etc/sysconfig/ i18n, keyboard, network files/variables to
  systemd native files

* Tue Oct 23 2012 Lennart Poettering <lpoetter@redhat.com> - 195-2
- Provide syslog because the journal is fine as a syslog implementation

* Tue Oct 23 2012 Lennart Poettering <lpoetter@redhat.com> - 195-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=831665
- https://bugzilla.redhat.com/show_bug.cgi?id=847720
- https://bugzilla.redhat.com/show_bug.cgi?id=858693
- https://bugzilla.redhat.com/show_bug.cgi?id=863481
- https://bugzilla.redhat.com/show_bug.cgi?id=864629
- https://bugzilla.redhat.com/show_bug.cgi?id=864672
- https://bugzilla.redhat.com/show_bug.cgi?id=864674
- https://bugzilla.redhat.com/show_bug.cgi?id=865128
- https://bugzilla.redhat.com/show_bug.cgi?id=866346
- https://bugzilla.redhat.com/show_bug.cgi?id=867407
- https://bugzilla.redhat.com/show_bug.cgi?id=868603

* Wed Oct 10 2012 Michal Schmidt <mschmidt@redhat.com> - 194-2
- Add scriptlets for migration away from systemd-timedated-ntp.target

* Wed Oct  3 2012 Lennart Poettering <lpoetter@redhat.com> - 194-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=859614
- https://bugzilla.redhat.com/show_bug.cgi?id=859655

* Fri Sep 28 2012 Lennart Poettering <lpoetter@redhat.com> - 193-1
- New upstream release

* Tue Sep 25 2012 Lennart Poettering <lpoetter@redhat.com> - 192-1
- New upstream release

* Fri Sep 21 2012 Lennart Poettering <lpoetter@redhat.com> - 191-2
- Fix journal mmap header prototype definition to fix compilation on 32bit

* Fri Sep 21 2012 Lennart Poettering <lpoetter@redhat.com> - 191-1
- New upstream release
- Enable all display managers by default, as discussed with Adam Williamson

* Thu Sep 20 2012 Lennart Poettering <lpoetter@redhat.com> - 190-1
- New upstream release
- Take possession of /etc/localtime, and remove /etc/sysconfig/clock
- https://bugzilla.redhat.com/show_bug.cgi?id=858780
- https://bugzilla.redhat.com/show_bug.cgi?id=858787
- https://bugzilla.redhat.com/show_bug.cgi?id=858771
- https://bugzilla.redhat.com/show_bug.cgi?id=858754
- https://bugzilla.redhat.com/show_bug.cgi?id=858746
- https://bugzilla.redhat.com/show_bug.cgi?id=858266
- https://bugzilla.redhat.com/show_bug.cgi?id=858224
- https://bugzilla.redhat.com/show_bug.cgi?id=857670
- https://bugzilla.redhat.com/show_bug.cgi?id=856975
- https://bugzilla.redhat.com/show_bug.cgi?id=855863
- https://bugzilla.redhat.com/show_bug.cgi?id=851970
- https://bugzilla.redhat.com/show_bug.cgi?id=851275
- https://bugzilla.redhat.com/show_bug.cgi?id=851131
- https://bugzilla.redhat.com/show_bug.cgi?id=847472
- https://bugzilla.redhat.com/show_bug.cgi?id=847207
- https://bugzilla.redhat.com/show_bug.cgi?id=846483
- https://bugzilla.redhat.com/show_bug.cgi?id=846085
- https://bugzilla.redhat.com/show_bug.cgi?id=845973
- https://bugzilla.redhat.com/show_bug.cgi?id=845194
- https://bugzilla.redhat.com/show_bug.cgi?id=845028
- https://bugzilla.redhat.com/show_bug.cgi?id=844630
- https://bugzilla.redhat.com/show_bug.cgi?id=839736
- https://bugzilla.redhat.com/show_bug.cgi?id=835848
- https://bugzilla.redhat.com/show_bug.cgi?id=831740
- https://bugzilla.redhat.com/show_bug.cgi?id=823485
- https://bugzilla.redhat.com/show_bug.cgi?id=821813
- https://bugzilla.redhat.com/show_bug.cgi?id=807886
- https://bugzilla.redhat.com/show_bug.cgi?id=802198
- https://bugzilla.redhat.com/show_bug.cgi?id=767795
- https://bugzilla.redhat.com/show_bug.cgi?id=767561
- https://bugzilla.redhat.com/show_bug.cgi?id=752774
- https://bugzilla.redhat.com/show_bug.cgi?id=732874
- https://bugzilla.redhat.com/show_bug.cgi?id=858735

* Thu Sep 13 2012 Lennart Poettering <lpoetter@redhat.com> - 189-4
- Don't pull in pkg-config as dep
- https://bugzilla.redhat.com/show_bug.cgi?id=852828

* Wed Sep 12 2012 Lennart Poettering <lpoetter@redhat.com> - 189-3
- Update preset policy
- Rename preset policy file from 99-default.preset to 90-default.preset so that people can order their own stuff after the Fedora default policy if they wish

* Thu Aug 23 2012 Lennart Poettering <lpoetter@redhat.com> - 189-2
- Update preset policy
- https://bugzilla.redhat.com/show_bug.cgi?id=850814

* Thu Aug 23 2012 Lennart Poettering <lpoetter@redhat.com> - 189-1
- New upstream release

* Thu Aug 16 2012 Ray Strode <rstrode@redhat.com> 188-4
- more scriptlet fixes
  (move dm migration logic to %%posttrans so the service
   files it's looking for are available at the time
   the logic is run)

* Sat Aug 11 2012 Lennart Poettering <lpoetter@redhat.com> - 188-3
- Remount file systems MS_PRIVATE before switching roots
- https://bugzilla.redhat.com/show_bug.cgi?id=847418

* Wed Aug 08 2012 Rex Dieter <rdieter@fedoraproject.org> - 188-2
- fix scriptlets

* Wed Aug  8 2012 Lennart Poettering <lpoetter@redhat.com> - 188-1
- New upstream release
- Enable gdm and avahi by default via the preset file
- Convert /etc/sysconfig/desktop to display-manager.service symlink
- Enable hardened build

* Mon Jul 30 2012 Kay Sievers <kay@redhat.com> - 187-3
- Obsolete: system-setup-keyboard

* Wed Jul 25 2012 Kalev Lember <kalevlember@gmail.com> - 187-2
- Run ldconfig for the new -libs subpackage

* Thu Jul 19 2012 Lennart Poettering <lpoetter@redhat.com> - 187-1
- New upstream release

* Mon Jul 09 2012 Harald Hoyer <harald@redhat.com> 186-2
- fixed dracut conflict version

* Tue Jul  3 2012 Lennart Poettering <lpoetter@redhat.com> - 186-1
- New upstream release

* Fri Jun 22 2012 Nils Philippsen <nils@redhat.com> - 185-7.gite7aee75
- add obsoletes/conflicts so multilib systemd -> systemd-libs updates work

* Thu Jun 14 2012 Michal Schmidt <mschmidt@redhat.com> - 185-6.gite7aee75
- Update to current git

* Wed Jun 06 2012 Kay Sievers - 185-5.gita2368a3
- disable plymouth in configure, to drop the .wants/ symlinks

* Wed Jun 06 2012 Michal Schmidt <mschmidt@redhat.com> - 185-4.gita2368a3
- Update to current git snapshot
  - Add systemd-readahead-analyze
  - Drop upstream patch
- Split systemd-libs
- Drop duplicate doc files
- Fixed License headers of subpackages

* Wed Jun 06 2012 Ray Strode <rstrode@redhat.com> - 185-3
- Drop plymouth files
- Conflict with old plymouth

* Tue Jun 05 2012 Kay Sievers - 185-2
- selinux udev labeling fix
- conflict with older dracut versions for new udev file names

* Mon Jun 04 2012 Kay Sievers - 185-1
- New upstream release
  - udev selinux labeling fixes
  - new man pages
  - systemctl help <unit name>

* Thu May 31 2012 Lennart Poettering <lpoetter@redhat.com> - 184-1
- New upstream release

* Thu May 24 2012 Kay Sievers <kay@redhat.com> - 183-1
- New upstream release including udev merge.

* Wed Mar 28 2012 Michal Schmidt <mschmidt@redhat.com> - 44-4
- Add triggers from Bill Nottingham to correct the damage done by
  the obsoleted systemd-units's preun scriptlet (#807457).

* Mon Mar 26 2012 Dennis Gilmore <dennis@ausil.us> - 44-3
- apply patch from upstream so we can build systemd on arm and ppc
- and likely the rest of the secondary arches

* Tue Mar 20 2012 Michal Schmidt <mschmidt@redhat.com> - 44-2
- Don't build the gtk parts anymore. They're moving into systemd-ui.
- Remove a dead patch file.

* Fri Mar 16 2012 Lennart Poettering <lpoetter@redhat.com> - 44-1
- New upstream release
- Closes #798760, #784921, #783134, #768523, #781735

* Mon Feb 27 2012 Dennis Gilmore <dennis@ausil.us> - 43-2
- don't conflict with fedora-release systemd never actually provided
- /etc/os-release so there is no actual conflict

* Wed Feb 15 2012 Lennart Poettering <lpoetter@redhat.com> - 43-1
- New upstream release
- Closes #789758, #790260, #790522

* Sat Feb 11 2012 Lennart Poettering <lpoetter@redhat.com> - 42-1
- New upstream release
- Save a bit of entropy during system installation (#789407)
- Don't own /etc/os-release anymore, leave that to fedora-release

* Thu Feb  9 2012 Adam Williamson <awilliam@redhat.com> - 41-2
- rebuild for fixed binutils

* Thu Feb  9 2012 Lennart Poettering <lpoetter@redhat.com> - 41-1
- New upstream release

* Tue Feb  7 2012 Lennart Poettering <lpoetter@redhat.com> - 40-1
- New upstream release

* Thu Jan 26 2012 Kay Sievers <kay@redhat.com> - 39-3
- provide /sbin/shutdown

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 39-2
- increment release

* Wed Jan 25 2012 Kay Sievers <kay@redhat.com> - 39-1.1
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Wed Jan 25 2012 Lennart Poettering <lpoetter@redhat.com> - 39-1
- New upstream release

* Sun Jan 22 2012 Michal Schmidt <mschmidt@redhat.com> - 38-6.git9fa2f41
- Update to a current git snapshot.
- Resolves: #781657

* Sun Jan 22 2012 Michal Schmidt <mschmidt@redhat.com> - 38-5
- Build against libgee06. Reenable gtk tools.
- Delete unused patches.
- Add easy building of git snapshots.
- Remove legacy spec file elements.
- Don't mention implicit BuildRequires.
- Configure with --disable-static.
- Merge -units into the main package.
- Move section 3 manpages to -devel.
- Fix unowned directory.
- Run ldconfig in scriptlets.
- Split systemd-analyze to a subpackage.

* Sat Jan 21 2012 Dan Horák <dan[at]danny.cz> - 38-4
- fix build on big-endians

* Wed Jan 11 2012 Lennart Poettering <lpoetter@redhat.com> - 38-3
- Disable building of gtk tools for now

* Wed Jan 11 2012 Lennart Poettering <lpoetter@redhat.com> - 38-2
- Fix a few (build) dependencies

* Wed Jan 11 2012 Lennart Poettering <lpoetter@redhat.com> - 38-1
- New upstream release

* Tue Nov 15 2011 Michal Schmidt <mschmidt@redhat.com> - 37-4
- Run authconfig if /etc/pam.d/system-auth is not a symlink.
- Resolves: #753160

* Wed Nov 02 2011 Michal Schmidt <mschmidt@redhat.com> - 37-3
- Fix remote-fs-pre.target and its ordering.
- Resolves: #749940

* Wed Oct 19 2011 Michal Schmidt <mschmidt@redhat.com> - 37-2
- A couple of fixes from upstream:
- Fix a regression in bash-completion reported in Bodhi.
- Fix a crash in isolating.
- Resolves: #717325

* Tue Oct 11 2011 Lennart Poettering <lpoetter@redhat.com> - 37-1
- New upstream release
- Resolves: #744726, #718464, #713567, #713707, #736756

* Thu Sep 29 2011 Michal Schmidt <mschmidt@redhat.com> - 36-5
- Undo the workaround. Kay says it does not belong in systemd.
- Unresolves: #741655

* Thu Sep 29 2011 Michal Schmidt <mschmidt@redhat.com> - 36-4
- Workaround for the crypto-on-lvm-on-crypto disk layout
- Resolves: #741655

* Sun Sep 25 2011 Michal Schmidt <mschmidt@redhat.com> - 36-3
- Revert an upstream patch that caused ordering cycles
- Resolves: #741078

* Fri Sep 23 2011 Lennart Poettering <lpoetter@redhat.com> - 36-2
- Add /etc/timezone to ghosted files

* Fri Sep 23 2011 Lennart Poettering <lpoetter@redhat.com> - 36-1
- New upstream release
- Resolves: #735013, #736360, #737047, #737509, #710487, #713384

* Thu Sep  1 2011 Lennart Poettering <lpoetter@redhat.com> - 35-1
- New upstream release
- Update post scripts
- Resolves: #726683, #713384, #698198, #722803, #727315, #729997, #733706, #734611

* Thu Aug 25 2011 Lennart Poettering <lpoetter@redhat.com> - 34-1
- New upstream release

* Fri Aug 19 2011 Harald Hoyer <harald@redhat.com> 33-2
- fix ABRT on service file reloading
- Resolves: rhbz#732020

* Wed Aug  3 2011 Lennart Poettering <lpoetter@redhat.com> - 33-1
- New upstream release

* Fri Jul 29 2011 Lennart Poettering <lpoetter@redhat.com> - 32-1
- New upstream release

* Wed Jul 27 2011 Lennart Poettering <lpoetter@redhat.com> - 31-2
- Fix access mode of modprobe file, restart logind after upgrade

* Wed Jul 27 2011 Lennart Poettering <lpoetter@redhat.com> - 31-1
- New upstream release

* Wed Jul 13 2011 Lennart Poettering <lpoetter@redhat.com> - 30-1
- New upstream release

* Thu Jun 16 2011 Lennart Poettering <lpoetter@redhat.com> - 29-1
- New upstream release

* Mon Jun 13 2011 Michal Schmidt <mschmidt@redhat.com> - 28-4
- Apply patches from current upstream.
- Fixes memory size detection on 32-bit with >4GB RAM (BZ712341)

* Wed Jun 08 2011 Michal Schmidt <mschmidt@redhat.com> - 28-3
- Apply patches from current upstream
- https://bugzilla.redhat.com/show_bug.cgi?id=709909
- https://bugzilla.redhat.com/show_bug.cgi?id=710839
- https://bugzilla.redhat.com/show_bug.cgi?id=711015

* Sat May 28 2011 Lennart Poettering <lpoetter@redhat.com> - 28-2
- Pull in nss-myhostname

* Thu May 26 2011 Lennart Poettering <lpoetter@redhat.com> - 28-1
- New upstream release

* Wed May 25 2011 Lennart Poettering <lpoetter@redhat.com> - 26-2
- Bugfix release
- https://bugzilla.redhat.com/show_bug.cgi?id=707507
- https://bugzilla.redhat.com/show_bug.cgi?id=707483
- https://bugzilla.redhat.com/show_bug.cgi?id=705427
- https://bugzilla.redhat.com/show_bug.cgi?id=707577

* Sat Apr 30 2011 Lennart Poettering <lpoetter@redhat.com> - 26-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=699394
- https://bugzilla.redhat.com/show_bug.cgi?id=698198
- https://bugzilla.redhat.com/show_bug.cgi?id=698674
- https://bugzilla.redhat.com/show_bug.cgi?id=699114
- https://bugzilla.redhat.com/show_bug.cgi?id=699128

* Thu Apr 21 2011 Lennart Poettering <lpoetter@redhat.com> - 25-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=694788
- https://bugzilla.redhat.com/show_bug.cgi?id=694321
- https://bugzilla.redhat.com/show_bug.cgi?id=690253
- https://bugzilla.redhat.com/show_bug.cgi?id=688661
- https://bugzilla.redhat.com/show_bug.cgi?id=682662
- https://bugzilla.redhat.com/show_bug.cgi?id=678555
- https://bugzilla.redhat.com/show_bug.cgi?id=628004

* Wed Apr  6 2011 Lennart Poettering <lpoetter@redhat.com> - 24-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=694079
- https://bugzilla.redhat.com/show_bug.cgi?id=693289
- https://bugzilla.redhat.com/show_bug.cgi?id=693274
- https://bugzilla.redhat.com/show_bug.cgi?id=693161

* Tue Apr  5 2011 Lennart Poettering <lpoetter@redhat.com> - 23-1
- New upstream release
- Include systemd-sysv-convert

* Fri Apr  1 2011 Lennart Poettering <lpoetter@redhat.com> - 22-1
- New upstream release

* Wed Mar 30 2011 Lennart Poettering <lpoetter@redhat.com> - 21-2
- The quota services are now pulled in by mount points, hence no need to enable them explicitly

* Tue Mar 29 2011 Lennart Poettering <lpoetter@redhat.com> - 21-1
- New upstream release

* Mon Mar 28 2011 Matthias Clasen <mclasen@redhat.com> - 20-2
- Apply upstream patch to not send untranslated messages to plymouth

* Tue Mar  8 2011 Lennart Poettering <lpoetter@redhat.com> - 20-1
- New upstream release

* Tue Mar  1 2011 Lennart Poettering <lpoetter@redhat.com> - 19-1
- New upstream release

* Wed Feb 16 2011 Lennart Poettering <lpoetter@redhat.com> - 18-1
- New upstream release

* Mon Feb 14 2011 Bill Nottingham <notting@redhat.com> - 17-6
- bump upstart obsoletes (#676815)

* Wed Feb  9 2011 Tom Callaway <spot@fedoraproject.org> - 17-5
- add macros.systemd file for %%{_unitdir}

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  9 2011 Lennart Poettering <lpoetter@redhat.com> - 17-3
- Fix popen() of systemctl, #674916

* Mon Feb  7 2011 Bill Nottingham <notting@redhat.com> - 17-2
- add epoch to readahead obsolete

* Sat Jan 22 2011 Lennart Poettering <lpoetter@redhat.com> - 17-1
- New upstream release

* Tue Jan 18 2011 Lennart Poettering <lpoetter@redhat.com> - 16-2
- Drop console.conf again, since it is not shipped in pamtmp.conf

* Sat Jan  8 2011 Lennart Poettering <lpoetter@redhat.com> - 16-1
- New upstream release

* Thu Nov 25 2010 Lennart Poettering <lpoetter@redhat.com> - 15-1
- New upstream release

* Thu Nov 25 2010 Lennart Poettering <lpoetter@redhat.com> - 14-1
- Upstream update
- Enable hwclock-load by default
- Obsolete readahead
- Enable /var/run and /var/lock on tmpfs

* Fri Nov 19 2010 Lennart Poettering <lpoetter@redhat.com> - 13-1
- new upstream release

* Wed Nov 17 2010 Bill Nottingham <notting@redhat.com> 12-3
- Fix clash

* Wed Nov 17 2010 Lennart Poettering <lpoetter@redhat.com> - 12-2
- Don't clash with initscripts for now, so that we don't break the builders

* Wed Nov 17 2010 Lennart Poettering <lpoetter@redhat.com> - 12-1
- New upstream release

* Fri Nov 12 2010 Matthias Clasen <mclasen@redhat.com> - 11-2
- Rebuild with newer vala, libnotify

* Thu Oct  7 2010 Lennart Poettering <lpoetter@redhat.com> - 11-1
- New upstream release

* Wed Sep 29 2010 Jesse Keating <jkeating@redhat.com> - 10-6
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Bill Nottingham <notting@redhat.com> - 10-5
- merge -sysvinit into main package

* Mon Sep 20 2010 Bill Nottingham <notting@redhat.com> - 10-4
- obsolete upstart-sysvinit too

* Fri Sep 17 2010 Bill Nottingham <notting@redhat.com> - 10-3
- Drop upstart requires

* Tue Sep 14 2010 Lennart Poettering <lpoetter@redhat.com> - 10-2
- Enable audit
- https://bugzilla.redhat.com/show_bug.cgi?id=633771

* Tue Sep 14 2010 Lennart Poettering <lpoetter@redhat.com> - 10-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=630401
- https://bugzilla.redhat.com/show_bug.cgi?id=630225
- https://bugzilla.redhat.com/show_bug.cgi?id=626966
- https://bugzilla.redhat.com/show_bug.cgi?id=623456

* Fri Sep  3 2010 Bill Nottingham <notting@redhat.com> - 9-3
- move fedora-specific units to initscripts; require newer version thereof

* Fri Sep  3 2010 Lennart Poettering <lpoetter@redhat.com> - 9-2
- Add missing tarball

* Fri Sep  3 2010 Lennart Poettering <lpoetter@redhat.com> - 9-1
- New upstream version
- Closes 501720, 614619, 621290, 626443, 626477, 627014, 627785, 628913

* Fri Aug 27 2010 Lennart Poettering <lpoetter@redhat.com> - 8-3
- Reexecute after installation, take ownership of /var/run/user
- https://bugzilla.redhat.com/show_bug.cgi?id=627457
- https://bugzilla.redhat.com/show_bug.cgi?id=627634

* Thu Aug 26 2010 Lennart Poettering <lpoetter@redhat.com> - 8-2
- Properly create default.target link

* Wed Aug 25 2010 Lennart Poettering <lpoetter@redhat.com> - 8-1
- New upstream release

* Thu Aug 12 2010 Lennart Poettering <lpoetter@redhat.com> - 7-3
- Fix https://bugzilla.redhat.com/show_bug.cgi?id=623561

* Thu Aug 12 2010 Lennart Poettering <lpoetter@redhat.com> - 7-2
- Fix https://bugzilla.redhat.com/show_bug.cgi?id=623430

* Tue Aug 10 2010 Lennart Poettering <lpoetter@redhat.com> - 7-1
- New upstream release

* Fri Aug  6 2010 Lennart Poettering <lpoetter@redhat.com> - 6-2
- properly hide output on package installation
- pull in coreutils during package installtion

* Fri Aug  6 2010 Lennart Poettering <lpoetter@redhat.com> - 6-1
- New upstream release
- Fixes #621200

* Wed Aug  4 2010 Lennart Poettering <lpoetter@redhat.com> - 5-2
- Add tarball

* Wed Aug  4 2010 Lennart Poettering <lpoetter@redhat.com> - 5-1
- Prepare release 5

* Tue Jul 27 2010 Bill Nottingham <notting@redhat.com> - 4-4
- Add 'sysvinit-userspace' provide to -sysvinit package to fix upgrade/install (#618537)

* Sat Jul 24 2010 Lennart Poettering <lpoetter@redhat.com> - 4-3
- Add libselinux to build dependencies

* Sat Jul 24 2010 Lennart Poettering <lpoetter@redhat.com> - 4-2
- Use the right tarball

* Sat Jul 24 2010 Lennart Poettering <lpoetter@redhat.com> - 4-1
- New upstream release, and make default

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> - 3-3
- Used wrong tarball

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> - 3-2
- Own /cgroup jointly with libcgroup, since we don't dpend on it anymore

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> - 3-1
- New upstream release

* Fri Jul 9 2010 Lennart Poettering <lpoetter@redhat.com> - 2-0
- New upstream release

* Wed Jul 7 2010 Lennart Poettering <lpoetter@redhat.com> - 1-0
- First upstream release

* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> - 0-0.7.20100629git4176e5
- New snapshot
- Split off -units package where other packages can depend on without pulling in the whole of systemd

* Tue Jun 22 2010 Lennart Poettering <lpoetter@redhat.com> - 0-0.6.20100622gita3723b
- Add missing libtool dependency.

* Tue Jun 22 2010 Lennart Poettering <lpoetter@redhat.com> - 0-0.5.20100622gita3723b
- Update snapshot

* Mon Jun 14 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.4.20100614git393024
- Pull the latest snapshot that fixes a segfault. Resolves rhbz#603231

* Fri Jun 11 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.3.20100610git2f198e
- More minor fixes as per review

* Thu Jun 10 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.2.20100610git2f198e
- Spec improvements from David Hollis

* Wed Jun 09 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.1.20090609git2f198e
- Address review comments

* Tue Jun 01 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.0.git2010-06-02
- Initial spec (adopted from Kay Sievers)
