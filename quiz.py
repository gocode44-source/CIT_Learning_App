for ch in chapters:
    st.write(f"## {ch['name']}")

    if st.button(f"Complete {ch['name']}"):
        complete_chapter(st.session_state.user, ch["name"], ch["xp"])
        st.success("Completed!")
        st.rerun()

    # Quiz
    if ch["name"] in quiz_data:
        for q in quiz_data[ch["name"]]:
            ans = st.radio(q["question"], q["options"], key=q["question"])

            if st.button("Submit", key=q["question"]+"btn"):
                if ans == q["answer"]:
                    st.success("Correct +30 XP")
                else:
                    st.error("Wrong")
