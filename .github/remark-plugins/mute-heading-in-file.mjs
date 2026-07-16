// remark-validate-links has no option to disable a single check kind (it only
// exposes repository/root/urlConfig). `missing-heading-in-file` false-positives
// on MkDocs `attr_list` heading ids (e.g. `{#complete-2025-hazard-list}`), which
// it can't parse, so we strip just that rule's messages once the link-check
// completer (which runs after every file's transform) has produced them.
export default function remarkMuteHeadingInFile(options, fileSet) {
  if (!fileSet) return

  fileSet.use(function completer(set) {
    for (const file of set.files) {
      file.messages = file.messages.filter(
        (message) => message.ruleId !== 'missing-heading-in-file'
      )
    }
  })
}
