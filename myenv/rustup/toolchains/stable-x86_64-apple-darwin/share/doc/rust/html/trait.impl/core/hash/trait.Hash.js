(function() {var implementors = {
"alloc":[["impl <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"alloc/ffi/struct.CString.html\" title=\"struct alloc::ffi::CString\">CString</a>"],["impl <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"alloc/string/struct.String.html\" title=\"struct alloc::string::String\">String</a>"],["impl&lt;B&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"enum\" href=\"alloc/borrow/enum.Cow.html\" title=\"enum alloc::borrow::Cow\">Cow</a>&lt;'_, B&gt;<div class=\"where\">where\n    B: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> + <a class=\"trait\" href=\"alloc/borrow/trait.ToOwned.html\" title=\"trait alloc::borrow::ToOwned\">ToOwned</a> + ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a>,</div>"],["impl&lt;K: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a>, V: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a>, A: <a class=\"trait\" href=\"alloc/alloc/trait.Allocator.html\" title=\"trait alloc::alloc::Allocator\">Allocator</a> + <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/clone/trait.Clone.html\" title=\"trait core::clone::Clone\">Clone</a>&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"alloc/collections/btree_map/struct.BTreeMap.html\" title=\"struct alloc::collections::btree_map::BTreeMap\">BTreeMap</a>&lt;K, V, A&gt;"],["impl&lt;T: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a>, A: <a class=\"trait\" href=\"alloc/alloc/trait.Allocator.html\" title=\"trait alloc::alloc::Allocator\">Allocator</a> + <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/clone/trait.Clone.html\" title=\"trait core::clone::Clone\">Clone</a>&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"alloc/collections/btree_set/struct.BTreeSet.html\" title=\"struct alloc::collections::btree_set::BTreeSet\">BTreeSet</a>&lt;T, A&gt;"],["impl&lt;T: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a>, A: <a class=\"trait\" href=\"alloc/alloc/trait.Allocator.html\" title=\"trait alloc::alloc::Allocator\">Allocator</a>&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"alloc/collections/linked_list/struct.LinkedList.html\" title=\"struct alloc::collections::linked_list::LinkedList\">LinkedList</a>&lt;T, A&gt;"],["impl&lt;T: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a>, A: <a class=\"trait\" href=\"alloc/alloc/trait.Allocator.html\" title=\"trait alloc::alloc::Allocator\">Allocator</a>&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"alloc/collections/vec_deque/struct.VecDeque.html\" title=\"struct alloc::collections::vec_deque::VecDeque\">VecDeque</a>&lt;T, A&gt;"],["impl&lt;T: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a>, A: <a class=\"trait\" href=\"alloc/alloc/trait.Allocator.html\" title=\"trait alloc::alloc::Allocator\">Allocator</a>&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"alloc/vec/struct.Vec.html\" title=\"struct alloc::vec::Vec\">Vec</a>&lt;T, A&gt;"],["impl&lt;T: ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a> + <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a>, A: <a class=\"trait\" href=\"alloc/alloc/trait.Allocator.html\" title=\"trait alloc::alloc::Allocator\">Allocator</a>&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"alloc/boxed/struct.Box.html\" title=\"struct alloc::boxed::Box\">Box</a>&lt;T, A&gt;"],["impl&lt;T: ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a> + <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a>, A: <a class=\"trait\" href=\"alloc/alloc/trait.Allocator.html\" title=\"trait alloc::alloc::Allocator\">Allocator</a>&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"alloc/rc/struct.Rc.html\" title=\"struct alloc::rc::Rc\">Rc</a>&lt;T, A&gt;"],["impl&lt;T: ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a> + <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a>, A: <a class=\"trait\" href=\"alloc/alloc/trait.Allocator.html\" title=\"trait alloc::alloc::Allocator\">Allocator</a>&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"alloc/sync/struct.Arc.html\" title=\"struct alloc::sync::Arc\">Arc</a>&lt;T, A&gt;"]],
"core":[],
"std":[["impl <a class=\"trait\" href=\"std/hash/trait.Hash.html\" title=\"trait std::hash::Hash\">Hash</a> for <a class=\"enum\" href=\"std/io/enum.ErrorKind.html\" title=\"enum std::io::ErrorKind\">ErrorKind</a>"],["impl <a class=\"trait\" href=\"std/hash/trait.Hash.html\" title=\"trait std::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"std/ffi/struct.OsStr.html\" title=\"struct std::ffi::OsStr\">OsStr</a>"],["impl <a class=\"trait\" href=\"std/hash/trait.Hash.html\" title=\"trait std::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"std/ffi/struct.OsString.html\" title=\"struct std::ffi::OsString\">OsString</a>"],["impl <a class=\"trait\" href=\"std/hash/trait.Hash.html\" title=\"trait std::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"std/fs/struct.FileType.html\" title=\"struct std::fs::FileType\">FileType</a>"],["impl <a class=\"trait\" href=\"std/hash/trait.Hash.html\" title=\"trait std::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"std/os/unix/net/struct.UCred.html\" title=\"struct std::os::unix::net::UCred\">UCred</a>"],["impl <a class=\"trait\" href=\"std/hash/trait.Hash.html\" title=\"trait std::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"std/path/struct.Path.html\" title=\"struct std::path::Path\">Path</a>"],["impl <a class=\"trait\" href=\"std/hash/trait.Hash.html\" title=\"trait std::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"std/path/struct.PathBuf.html\" title=\"struct std::path::PathBuf\">PathBuf</a>"],["impl <a class=\"trait\" href=\"std/hash/trait.Hash.html\" title=\"trait std::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"std/path/struct.PrefixComponent.html\" title=\"struct std::path::PrefixComponent\">PrefixComponent</a>&lt;'_&gt;"],["impl <a class=\"trait\" href=\"std/hash/trait.Hash.html\" title=\"trait std::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"std/thread/struct.ThreadId.html\" title=\"struct std::thread::ThreadId\">ThreadId</a>"],["impl <a class=\"trait\" href=\"std/hash/trait.Hash.html\" title=\"trait std::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"std/time/struct.Instant.html\" title=\"struct std::time::Instant\">Instant</a>"],["impl <a class=\"trait\" href=\"std/hash/trait.Hash.html\" title=\"trait std::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"std/time/struct.SystemTime.html\" title=\"struct std::time::SystemTime\">SystemTime</a>"],["impl&lt;'a&gt; <a class=\"trait\" href=\"std/hash/trait.Hash.html\" title=\"trait std::hash::Hash\">Hash</a> for <a class=\"enum\" href=\"std/path/enum.Component.html\" title=\"enum std::path::Component\">Component</a>&lt;'a&gt;"],["impl&lt;'a&gt; <a class=\"trait\" href=\"std/hash/trait.Hash.html\" title=\"trait std::hash::Hash\">Hash</a> for <a class=\"enum\" href=\"std/path/enum.Prefix.html\" title=\"enum std::path::Prefix\">Prefix</a>&lt;'a&gt;"]],
"test":[["impl <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"enum\" href=\"test/enum.NamePadding.html\" title=\"enum test::NamePadding\">NamePadding</a>"],["impl <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"enum\" href=\"test/test/enum.ShouldPanic.html\" title=\"enum test::test::ShouldPanic\">ShouldPanic</a>"],["impl <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"enum\" href=\"test/test/enum.TestName.html\" title=\"enum test::test::TestName\">TestName</a>"],["impl <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"enum\" href=\"test/test/enum.TestType.html\" title=\"enum test::test::TestType\">TestType</a>"],["impl <a class=\"trait\" href=\"https://doc.rust-lang.org/1.80.1/core/hash/trait.Hash.html\" title=\"trait core::hash::Hash\">Hash</a> for <a class=\"struct\" href=\"test/test/struct.TestId.html\" title=\"struct test::test::TestId\">TestId</a>"]]
};if (window.register_implementors) {window.register_implementors(implementors);} else {window.pending_implementors = implementors;}})()