import sys
import re

with open("crates/librefang-types/src/taint.rs", "r") as f:
    code = f.read()

# 1. Update TaintedValue struct
old_struct = """pub struct TaintedValue {
    /// The actual string payload.
    pub value: String,
    /// The set of taint labels currently attached.
    pub labels: HashSet<TaintLabel>,
    /// Human-readable description of where this value originated.
    pub source: String,
}"""
new_struct = """pub struct TaintedValue<T> {
    /// The actual payload.
    pub value: T,
    /// The set of taint labels currently attached.
    pub labels: HashSet<TaintLabel>,
    /// Human-readable description(s) of where this value originated.
    pub sources: std::collections::BTreeSet<String>,
}"""
code = code.replace(old_struct, new_struct)

# 2. Update TaintedValue impl
old_impl = """impl TaintedValue {
    /// Creates a new tainted value with the given labels.
    pub fn new(
        value: impl Into<String>,
        labels: HashSet<TaintLabel>,
        source: impl Into<String>,
    ) -> Self {
        Self {
            value: value.into(),
            labels,
            source: source.into(),
        }
    }

    /// Creates a clean (untainted) value with no labels.
    pub fn clean(value: impl Into<String>, source: impl Into<String>) -> Self {
        Self {
            value: value.into(),
            labels: HashSet::new(),
            source: source.into(),
        }
    }

    /// Merges the taint labels from `other` into this value.
    ///
    /// This is used when two values are concatenated or otherwise combined;
    /// the result must carry the union of both label sets.
    pub fn merge_taint(&mut self, other: &TaintedValue) {
        for label in &other.labels {
            self.labels.insert(label.clone());
        }
    }

    /// Checks whether this value is safe to flow into the given sink.
    ///
    /// Returns `Ok(())` if none of the value's labels are blocked by the
    /// sink, or `Err(TaintViolation)` describing the first conflict found.
    pub fn check_sink(&self, sink: &TaintSink) -> Result<(), TaintViolation> {
        for label in &self.labels {
            if sink.blocked_labels.contains(label) {
                return Err(TaintViolation {
                    label: label.clone(),
                    sink_name: sink.name.clone(),
                    source: self.source.clone(),
                });
            }
        }
        Ok(())
    }"""
    
new_impl = """impl<T> TaintedValue<T> {
    /// Creates a new tainted value with the given labels.
    pub fn new(
        value: T,
        labels: HashSet<TaintLabel>,
        source: impl Into<String>,
    ) -> Self {
        let mut sources = std::collections::BTreeSet::new();
        sources.insert(source.into());
        Self {
            value,
            labels,
            sources,
        }
    }

    /// Creates a clean (untainted) value with no labels.
    pub fn clean(value: T, source: impl Into<String>) -> Self {
        let mut sources = std::collections::BTreeSet::new();
        sources.insert(source.into());
        Self {
            value,
            labels: HashSet::new(),
            sources,
        }
    }

    /// Merges the taint labels from `other` into this value.
    ///
    /// This is used when two values are concatenated or otherwise combined;
    /// the result must carry the union of both label sets.
    pub fn merge_taint<U>(&mut self, other: &TaintedValue<U>) {
        for label in &other.labels {
            self.labels.insert(label.clone());
        }
        for source in &other.sources {
            self.sources.insert(source.clone());
        }
    }

    /// Maps the inner value using the provided function, preserving all taint labels and sources.
    pub fn map<U, F: FnOnce(T) -> U>(self, f: F) -> TaintedValue<U> {
        TaintedValue {
            value: f(self.value),
            labels: self.labels,
            sources: self.sources,
        }
    }

    /// Flat-maps the inner value using the provided function.
    /// The resulting `TaintedValue` combines the labels and sources of both values.
    pub fn bind<U, F: FnOnce(T) -> TaintedValue<U>>(self, f: F) -> TaintedValue<U> {
        let mut res = f(self.value);
        for label in self.labels {
            res.labels.insert(label);
        }
        for source in self.sources {
            res.sources.insert(source);
        }
        res
    }

    /// Checks whether this value is safe to flow into the given sink.
    ///
    /// Returns `Ok(())` if none of the value's labels are blocked by the
    /// sink, or `Err(TaintViolation)` describing the first conflict found.
    pub fn check_sink(&self, sink: &TaintSink) -> Result<(), TaintViolation> {
        for label in &self.labels {
            if sink.blocked_labels.contains(label) {
                let source_list: Vec<String> = self.sources.iter().cloned().collect();
                return Err(TaintViolation {
                    label: label.clone(),
                    sink_name: sink.name.clone(),
                    source: source_list.join(", "),
                });
            }
        }
        Ok(())
    }"""
code = code.replace(old_impl, new_impl)

with open("crates/librefang-types/src/taint.rs", "w") as f:
    f.write(code)
